from app import app,db, socketio
from view import login_required, need_profile_info
from flask import render_template, redirect, url_for, g, request
from user import User
from functions import get_user_photos, get_user_tags
from datetime import datetime
from flask_socketio import SocketIO, emit, send
import json

@app.route("/user_page/<member>", methods=["GET", "POST"])
@login_required
@need_profile_info
def user_page(member):
    if g.user.id == member:
        return redirect(url_for('profile'))
    try:
        member = int(member)
    except:
        return redirect(url_for('index'))
    user = User.get_filter(id=member)[0]
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM notifications WHERE whom=%s AND type='msg'", (g.user.id, )) #удаление уведомления о новом сообщении
    cursor.execute("SELECT who FROM visits WHERE who=%s AND whom=%s", (g.user.id, user.id))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO visits (who, whom) VALUES(%s, %s)", (g.user.id, user.id, ))
    else:
        cursor.execute("DELETE FROM visits WHERE who=%s AND whom=%s", (g.user.id, user.id, ))
        cursor.execute("INSERT INTO visits (who, whom) VALUES(%s, %s)", (g.user.id, user.id,))
    cursor.execute("SELECT who FROM blacklist WHERE who=%s AND whom=%s", (user.id, g.user.id, ))#### добавление в уведомления
    if not cursor.fetchone():
        cursor.execute("SELECT who FROM notifications WHERE who=%s AND whom=%s AND type='checked'", (g.user.id, user.id, ))
        if not cursor.fetchall():
            cursor.execute("INSERT INTO notifications (who, whom, type) VALUES(%s,%s,%s)", (g.user.id, user.id, 'checked', )) #### добавление в уведомления
    db.connection.commit()
    photos = get_user_photos(id=member)
    tags = get_user_tags(id=member)
    online = (datetime.now() - user.last_seen).seconds
    if online > 60:
        online = "Last online is " + str(user.last_seen)
    else:
        online="online"
    cursor.execute("SELECT who FROM likes WHERE who=%s AND whom=%s", (g.user.id, user.id, ))
    if cursor.fetchall():
        dislike="dislike"
    else:
        dislike=None
    cursor.execute("SELECT who FROM blacklist WHERE who=%s AND whom=%s", (g.user.id, user.id, ))
    if cursor.fetchall():
        blacklist = "blacklist"
    else:
        blacklist = None
    cursor.execute("SELECT EXISTS(SELECT * FROM matches WHERE user1=%s AND user2=%s OR user1=%s AND user2=%s)", (g.user.id, user.id, user.id, g.user.id, ))
    if cursor.fetchone()[0]:
        cursor.execute("SELECT * FROM messages WHERE who=%s AND whom=%s OR who=%s AND whom=%s",(g.user.id, user.id, user.id, g.user.id, ))
        res = cursor.fetchall()
        msg = []
        for i in res:
            if i[0] == g.user.id:
                msg.append("<p style='text-align: right; color: blue; font-size: large;'>" + i[1] +  "</p>")
            else:
                msg.append("<p style='text-align: left; color: green; font-size: large;'>" + i[1] +  "</p>")
        match = True
    else:
        match = None
        msg = []
    return render_template('user_page.html', user=user, photos=photos, tags=tags, online=online, dislike=dislike, blacklist=blacklist, match=match, msg=msg)

@app.route('/like_manager', methods=['POST'])
@login_required
def like_manager():
    if request.method == "POST" and request.is_xhr and 'like' in request.form and 'whom' in request.form:
        cursor = db.connection.cursor()
        match = None
        cursor.execute("SELECT who FROM blacklist WHERE who=%s AND whom=%s", (request.form['whom'], g.user.id, ))#### добавление в уведомления
        black = cursor.fetchall()    ######уведомления
        if (request.form['like'] == "like"):
            cursor.execute("SELECT who FROM likes WHERE who=%s AND whom=%s", (g.user.id, request.form['whom'], ))
            if not cursor.fetchall():
                cursor.execute("INSERT INTO likes (who, whom) VALUES(%s,%s)", (g.user.id, request.form['whom'], ))
                if not black:
                    cursor.execute("INSERT INTO notifications (who, whom, type) VALUES(%s,%s,%s)", (g.user.id, request.form['whom'], 'liked', )) ### уведомления
                cursor.execute("SELECT who FROM likes WHERE who=%s AND whom=%s", (request.form['whom'], g.user.id, )) # если тот кому мы ставим лайк, уже поставил лайк нам.
                if cursor.fetchall():
                    cursor.execute("INSERT INTO matches (user1, user2) VALUES(%s, %s)", (g.user.id, request.form['whom'], )) # если лайк есть, то MATCH
                    if not black:
                        cursor.execute("INSERT INTO notifications (who, whom, type) VALUES(%s,%s,%s)", (g.user.id, request.form['whom'], 'match', )) ### уведомления
                    match = True
        if (request.form['like'] == 'dislike'):
            cursor.execute("DELETE FROM likes WHERE who=%s AND whom=%s", (g.user.id, request.form['whom'], ))
            cursor.execute("SELECT user1 FROM matches WHERE user1=%s AND user2=%s OR user1=%s AND user2=%s", (g.user.id, request.form['whom'], request.form['whom'], g.user.id, ))
            if cursor.fetchone():
                cursor.execute("DELETE FROM matches WHERE user1=%s AND user2=%s OR user1=%s AND user2=%s", (g.user.id, request.form['whom'], request.form['whom'], g.user.id, ))
                cursor.execute("DELETE FROM messages WHERE who=%s AND whom=%s OR who=%s AND whom=%s", (g.user.id, request.form['whom'], request.form['whom'], g.user.id, ))
                if not black:
                    cursor.execute("INSERT INTO notifications (who, whom, type) VALUES(%s,%s,%s)", (g.user.id, request.form['whom'], 'dislike', )) ### уведомления
                match = True # нужно проверить был ли вообще match
        db.connection.commit()
        cursor.close()
        if match:
            return 'show_chat'
        elif request.form['like'] == 'dislike':
            return 'show_like'
        else:
            return "show_dislike"
    return redirect(url_for('profile'))

@app.route('/blacklist_manager', methods=['POST'])
@login_required
def blacklist_manager(): ##### нужно ли сбрасывать лайк?
    if request.method == "POST" and request.is_xhr and 'blacklist' in request.form and 'whom' in request.form:
        cursor = db.connection.cursor()
        if (request.form['blacklist'] == "add_blacklist"):
            cursor.execute("SELECT who FROM blacklist WHERE who=%s AND whom=%s", (g.user.id, request.form['whom'], ))
            if not cursor.fetchall():
                cursor.execute("INSERT INTO blacklist (who, whom) VALUES(%s,%s)", (g.user.id, request.form['whom'], ))
        if (request.form['blacklist'] == 'delete_blacklist'):
            cursor.execute("DELETE FROM blacklist WHERE who=%s AND whom=%s", (g.user.id, request.form['whom'], ))
        db.connection.commit()
        cursor.close()
        return "show_add" if request.form['blacklist'] == 'delete_blacklist' else "show_delete"
    return redirect(url_for('profile'))

@app.route('/report_as_fake', methods=['POST']) ### плохо реализовано!
@login_required
def report_as_fake():
    if request.method == "POST" and request.is_xhr and "whom" in request.form:
        cursor = db.connection.cursor()
        cursor.execute("SELECT who FROM reports WHERE who=%s AND whom=%s", (g.user.id, request.form['whom'], ))
        if not cursor.fetchall():
            cursor.execute("INSERT INTO reports (who, whom) VALUES(%s,%s)", (g.user.id, request.form['whom'], ))
            db.connection.commit()
        cursor.close()
        return ("ok")
    return redirect(url_for('index'))

@socketio.on('message', namespace="/chat")
def message_func(msg):
    cursor = db.connection.cursor()
    if type(msg) is list:
        cursor.execute("INSERT INTO messages (who, msg, whom) VALUES(%s, %s, %s)", (msg[2], msg[1], msg[0], ))
        cursor.execute("SELECT who FROM blacklist WHERE who=%s AND whom=%s", (msg[0], msg[2], ))#### добавление в уведомления
        if not cursor.fetchall():
            cursor.execute("INSERT INTO notifications (who, whom, type) VALUES(%s,%s,%s)", (msg[2], msg[0], 'msg', )) ### уведомления
        db.connection.commit()
    send(json.dumps(msg), broadcast=True, namespace="/" + msg[2] + "_" + msg[0])
    send(json.dumps(msg), broadcast=True, namespace="/" + msg[0] + "_" + msg[2])


@app.route("/show_notifications", methods=['GET', 'POST'])
@login_required
def show_notifications():
    if request.method == "POST" and request.is_xhr:
        cursor = db.connection.cursor()
        cursor.execute("SELECT count(who) FROM notifications WHERE whom=%s", (g.user.id, ))
        res = cursor.fetchone()[0]
        cursor.execute("SELECT who, type FROM notifications WHERE whom=%s LIMIT 1", (g.user.id, ))
        return json.dumps([str(res), cursor.fetchone()])
    return redirect(url_for('index'))





