from app import app, db
from flask import render_template, g, request, redirect, url_for, session
from user import User
from geopy import Nominatim
from view import login_required, need_profile_info


@app.route('/matches')
@login_required
@need_profile_info
def matches():
    dic = {}
    dic['id!'] = g.user.id
    dic['JUST_ADD'] = " AND id IN (SELECT user1 FROM matches WHERE user2={}) OR id IN (SELECT user2 FROM matches WHERE user1={})".format(g.user.id, g.user.id)
    users = User.get_filter(**dic)
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM notifications WHERE whom=%s AND type='match' OR type='dislike'", (g.user.id, )) # удаление уведомлений о дизлайке или матче
    db.connection.commit()
    return render_template('matches.html', users=users)