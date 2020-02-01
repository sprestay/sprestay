from app import app, db
from flask import render_template, redirect, request, url_for, session
import json, re, random, string, hashlib
from functions import send_mail


def username_checker(content):
    response = []
    if len(content) < 3:
        response.append('Too short, min length is 3')
    if len(content) > 20:
        response.append('Sorry, 20 symbols max')
    if not content.isalnum():
        response.append('Only letters and numbers')
    if not response:
        cursor = db.connection.cursor()
        cursor.execute("SELECT username FROM account WHERE username=%s", (content,))
        res = cursor.fetchall()
        if not res:
            return('ok')
        else:
            return(json.dumps(['This username is already in use']))
    else:
        return(json.dumps(response))

def email_checker(content):
    valid = re.match(r'(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)', content)
    if len(content) > 100:
        return json.dumps('Too long')
    if not valid:
        return json.dumps(['Seems your email is incorrect'])
    cursor = db.connection.cursor()
    cursor.execute("SELECT email FROM account WHERE email=%s", (content,))
    res = cursor.fetchall()
    if not res:
        return ('ok')
    else:
        return (json.dumps(['This email already in use!']))

def check_password(content):
    response = []
    if len(content) < 6:
        response.append('Minimum length is 6 chars')
    if len(content) > 15:
        response.append('Sorry, it`s too long')
    if not re.match(r'(?=.*[0-9])(?=.*[!?_:%&$#@])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!?_:%&$#@]', content):
        response.append('At least one from every:')
        response.append('a-z, A-Z, 0-9, [ !?_:%&$#@ ]')
    if not response:
        return ('ok')
    else:
        return json.dumps(response)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.is_xhr:
        if (request.form['element'] == 'username'):
            return username_checker(request.form['content'])
        if (request.form['element'] == 'inputFirst' or request.form['element'] == 'inputSecond'):
            if (len(request.form['content']) > 20):
                return json.dumps(['Sorry, 20 symbols max'])
            if (request.form['content'].isalpha()):
                return ('ok')
            else:
                return (json.dumps(['Only letters are allowed!']))
        if (request.form['element'] == 'inputEmailR'):
            return email_checker(request.form['content'])
        if (request.form['element'].startswith('inputPassword')):
            return check_password(request.form['content'])
        
        return ('ok')
    return render_template('login/base.html')

@app.route('/create_user', methods=['POST']) # запись в бд. Без проверок!
def create_user():
    if request.method == "POST":
        form = request.form
        confirm = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(20))
        p_hash = hashlib.sha256(form['password'].encode()).hexdigest()
        insert = 'INSERT INTO account (username, first_name, second_name, email, confirm, password) VALUES(%s,%s,%s,%s,%s,%s)'
        try:
            cursor = db.connection.cursor()
            cursor.execute(insert, (form['username'], form['first_name'].capitalize(), form['second_name'].capitalize(), form['email'], confirm, p_hash))
            db.connection.commit()
            cursor.close()
        except:
            return render_template('login/error.html', error='Error while insert data into table')
        href = "<a href='" + request.url_root + 'activate/' + confirm + "'>Validate your email</a>"
        send_mail(form['email'], "Verification email", href)
        session['verif_was_sent'] = 'true'
    return redirect(url_for('login'))

@app.route('/activate/<code>') #активация аккаунта по ссылке из пиьсма
def activate(code):
    cursor = db.connection.cursor()
    cursor.execute("SELECT username FROM account WHERE confirm=%s", (code,))
    res = cursor.fetchone() #внимание!
    if res:
        session['username'] = res[0]
        session['verif_was_sent'] = None
        cursor.execute("UPDATE account SET confirm='confirm' WHERE confirm=%s", (code,))
    db.connection.commit()
    cursor.close()
    return redirect('/')

@app.route('/sign_check', methods=['POST'])#логин
def sign_check():
    if request.method == 'POST' and request.is_xhr:
        p_hash = hashlib.sha256(request.form['password'].encode()).hexdigest()
        cursor = db.connection.cursor()
        cursor.execute("SELECT username FROM account WHERE username=%s AND password=%s AND confirm='confirm'", (request.form['username'], p_hash)) #дописать confirm=confirm
        res = cursor.fetchone()
        cursor.close()
        if not res:
            return ('error')
        else:
            session['username'] = request.form['username']
            session['verif_was_sent'] = None
            return ('ok')
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])#логаут
def logout():
    session['username'] = None
    return redirect('/')
    # return render_template('login/base.html')# redirect(?)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.is_xhr and request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        if len(username) < 3 or len(username) > 20 or not username.isalnum():
            return ("error")
        valid = re.match(r'(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)', email)
        if len(email) > 100 or not valid:
            return ('error')
        cursor = db.connection.cursor()
        cursor.execute("SELECT id FROM account WHERE username=%s AND email=%s", (username, email))
        user_id = cursor.fetchall()[0]
        if not user_id:
            return ('error')
        else:
            new_pass = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(8))
            cursor.execute("UPDATE account SET password=%s WHERE id=%s", (hashlib.sha256(new_pass.encode()).hexdigest(), user_id))
            db.connection.commit()
            cursor.close()
            send_mail(email, "Change password for matcha", 'Here is your new password - {}, dont forget to change it after login'.format(new_pass))
            return ('ok')
    return render_template('login/forgot.html')

