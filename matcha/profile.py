from app import app, db
from view import login_required
from flask import redirect, render_template, url_for, session, request, g
from user import User
from functions import send_mail, get_user_photos, get_user_tags
import random, string, hashlib, os, geocoder, json
from datetime import datetime
from geopy.geocoders import Nominatim

@app.route('/profile', methods=['GET', 'POST']) # отрисовка главной страницы + изменение данных аккаунта
@login_required
def profile():
    if request.method == "POST":
        dic = {}
        if (request.form['username']):
            dic['username'] = request.form['username']
            session['username'] = request.form['username']
        if (request.form['first_name']):
            dic['first_name'] = request.form['first_name']
        if (request.form['second_name']):
            dic['second_name'] = request.form['second_name']
        if (request.form['email']):
            cursor = db.connection.cursor()
            confirm = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(20))
            cursor.execute("INSERT INTO tmp_email (user_id, email, confirm) VALUES(%s,%s,%s)", (str(g.user.id), request.form['email'], confirm))
            href = "<a href='" + request.url_root + 'update_email/' + confirm + "'>Validate your new email</a>"
            send_mail(request.form['email'], "Update email", href)
            db.connection.commit()
            cursor.close()
            session['update_email_was_send'] = True
        if (request.form['password']):
            dic['password'] = hashlib.sha256(request.form['password'].encode()).hexdigest()
        if (dic):
            g.user.update(**dic)
        return redirect('/')
    user_tags = get_user_tags(id=g.user.id)
    tags = get_user_tags() ####### возможно уже не надо
    photos = get_user_photos(id=g.user.id)
    geo = Nominatim(timeout=5)
    city=""
    try:
        location = geo.reverse("" + str(g.user.coords[0]) + ", " + str(g.user.coords[1]))
        if 'city' in location.raw['address']:
            city=location.raw['address']['city']
        else:
            city=location.raw['address']['state']
    except:
        print("Error: geocode failed on timeout")
    if not city:
        city="Timeout error"
    return render_template('profile.html', photos=photos, user_tags=user_tags, tags=tags, city=city)

@app.route('/update_email/<code>') #подтверждение нового мейла
@login_required
def update_email(code):
    cursor = db.connection.cursor()
    cursor.execute("SELECT email from tmp_email WHERE confirm=%s AND user_id=%s", (code, str(g.user.id), ))
    res = cursor.fetchall()
    if res:
        g.user.update(email=res[0][0])
        session['update_email_was_send'] = None
        cursor.execute("DELETE FROM tmp_email WHERE user_id=%s", (str(g.user.id), ))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('profile'))
    cursor.close()
    return redirect('/')

@app.route('/profile_data', methods=['GET', 'POST']) #загрузка фото
@login_required
def profile_data():
    if request.method == "POST":
        dic = {}
        if 'gender' in request.form:
            if request.form['gender'] == 'm' or request.form['gender'] == 'w':
                dic['gender'] = request.form['gender']
        if 'orient' in request.form:
            if request.form['orient'] == 'hetero' or request.form['orient'] == 'homo' or request.form['orient'] == 'bi':
                dic['orient'] = request.form['orient']
        if "birth" in request.form:
            data = request.form['birth'].split('-')
            birth = datetime(int(data[0]),int(data[1]), int(data[2]))
            age = (datetime.now() - birth).total_seconds() / 31556952
            if age >= 18:
                dic['birth'] = request.form['birth']
        if "bio" in request.form:
            dic['bio'] = request.form['bio'].rstrip()
        if dic:
            g.user.update(**dic)
        if 'file' in request.files:
            cursor = db.connection.cursor()
            cursor.execute("SELECT count(src) FROM images WHERE id=%s", (str(g.user.id), ))
            res = cursor.fetchone()
            if (int(res[0]) >=5):
                return redirect(url_for('profile'))
            new_file = request.files['file']
            if new_file and new_file.mimetype in ['image/jpeg', 'image/png',]:
                os.makedirs(app.config['UPLOAD_FOLDER'] + session['username'], exist_ok=True)
                name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S.") + new_file.filename.rsplit('.',1)[1]
                new_file.save(os.path.join(app.config['UPLOAD_FOLDER'] + session['username'] + '/', name))
                cursor.execute("INSERT INTO images (id, src) VALUES(%s, %s)", (str(g.user.id), session['username'] + '/' + name,))
                db.connection.commit()
                cursor.close()
                return redirect(url_for('profile'))
            new_file.close()
        return redirect(url_for('profile'))
    return redirect(url_for('profile'))

@app.route('/delete_photo', methods=['GET','POST']) #удаление фото через ajax
@login_required
def delete_photo():
    if request.method == "POST" and request.is_xhr:
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM images WHERE id=%s AND src=%s", (str(g.user.id), request.form['delete']))
        db.connection.commit()
        cursor.execute("SELECT src FROM images WHERE id=%s", (str(g.user.id), ))
        res = cursor.fetchall()
        cursor.close()
        if res:
            return "ok"
        if not res:
            return "empty"
    return redirect(url_for('profile'))

@app.route('/add_tag/<tag_id>')
@login_required
def add_tag(tag_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT tg_id FROM tags WHERE title=%s", (tag_id, ))
    res = cursor.fetchone()
    if res:
        res = res[0]
        cursor.execute("SELECT us_id FROM user_tag WHERE us_id=%s AND tg_id=%s", (g.user.id, res, ))
        if not cursor.fetchall():
            cursor.execute("INSERT INTO user_tag (us_id, tg_id) VALUES(%s,%s)", (g.user.id, res, ))
        db.connection.commit()
        cursor.close()
    return redirect(url_for('profile'))

@app.route('/delete_tag/<tag_id>')
@login_required
def delete_tag(tag_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT tg_id FROM tags WHERE title=%s", (tag_id, ))
    res = cursor.fetchone()
    if res:
        res = res[0]
        cursor.execute("DELETE FROM user_tag WHERE us_id=%s AND tg_id=%s", (g.user.id, res, ))
        db.connection.commit()
        cursor.close()
    return redirect(url_for('profile'))

@app.route('/set_location', methods=['GET', 'POST'])
@login_required
def set_location():
    if request.method == "POST":
        if 'city' in request.form and 'location' in request.form:
            g.user.update(manually=1)
            g.user.manually=1
        elif not request.form:
            g.user.update(manually=0)
            g.user.manually=0
            ip = request.remote_addr #######вставка
            if ip == "127.0.0.1": ### надо ли?
                g.user.update(X="55.797208", Y="37.579750") 
            else:
                geo_ip = geocoder.ip(ip)
                g.user.update(X=geo_ip.latlng[0], Y=geo_ip.latlng[1]) ### конец вставки!
            return redirect(url_for('profile'))
    if request.method == "POST" and not g.user.manually and request.is_xhr:
        if 'lat' in request.form and 'lon' in request.form:
            g.user.update(X=request.form['lat'], Y=request.form['lon'])
            return ("ok")
        elif 'deny' in request.form:
            ip = request.remote_addr
            if ip == "127.0.0.1":
                g.user.update(X="55.797208", Y="37.579750")
            else:
                geo_ip = geocoder.ip(ip)
                g.user.update(X=geo_ip.latlng[0], Y=geo_ip.latlng[1])
            return ("ok")
        else:
            return ("error")
    if request.method == "POST" and g.user.manually:
        geo = Nominatim(timeout=5)
        location = geo.geocode(request.form['city'])
        if location:
            g.user.update(X=location.latitude, Y=location.longitude)
        return redirect(url_for('profile'))
    return redirect(url_for('profile'))


@app.route("/show_history", methods=['POST'])
def show_history():
    if request.method == "POST" and request.is_xhr:
        cursor = db.connection.cursor()
        cursor.execute("SELECT id, first_name FROM account JOIN visits ON account.id=visits.who AND visits.whom=%s", (g.user.id, ))
        res = cursor.fetchall()
        cursor.execute("DELETE FROM notifications WHERE whom=%s AND type='checked'", (g.user.id, )) # удаление уведомлений о просмотре
        cursor.execute("SELECT id, first_name FROM account JOIN likes ON account.id=likes.who AND likes.whom=%s", (g.user.id, ))
        likes = cursor.fetchall()
        cursor.execute("DELETE FROM notifications WHERE whom=%s AND type='liked'", (g.user.id, )) # удаление уведомлений о лайке

        db.connection.commit()
        cursor.close()
        if res: # jinja не генерирует ссылку в js
            resp = []
            for i in res:
                tmp = []
                tmp.append(str(url_for('user_page', member=i[0])))
                tmp.append(i[1])
                resp.append(tmp)
        else:
           resp = "Nothing =("
        if likes:
            lk = []
            for i in likes:
                tmp = []
                tmp.append(str(url_for('user_page', member=i[0])))
                tmp.append(i[1])
                lk.append(tmp)
        else:
            lk = "Nothing =("
        return json.dumps([resp, lk])
    return redirect(url_for('profile'))