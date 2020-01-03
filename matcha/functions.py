from datetime import datetime
import smtplib
from app import app, db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dateutil.relativedelta import relativedelta
from math import radians, cos, sin, asin, sqrt

def get_age(str_data):
    if str_data:
        data = str(str_data).split('-')
        birth = datetime(int(data[0]),int(data[1]), int(data[2]))
        return int((datetime.now() - birth).total_seconds() / 31556952)
    else:
        return -1

def send_mail(to, theme, text):                                
    
    password  = app.config['ADDRESANT_PASSWD']
    msg = MIMEMultipart()                               
    msg['From'] = app.config['ADDRESANT']                        
    msg['To'] = to                         
    msg['Subject'] = theme               

    body = text
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(app.config['ADDRESANT'], password)
    server.send_message(msg)
    server.quit()

def yearsago(years, from_date=None): 
    if from_date is None: from_date = datetime.now()
    return (from_date - relativedelta(years=years)).strftime("%Y-%m-%d")

def haversine(lat1, lon1, lat2, lon2): #расстояние между координатами
    if lat1 and lon1 and lat2 and lon2:
        lon1 = radians(lon1)
        lat1 = radians(lat1)# разберись с map
        lon2 = radians(lon2)
        lat2 = radians(lat2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return int(6367 * c)
    return -1

def get_user_photos(id=None, limit=None):
    if id:
        cursor = db.connection.cursor()
        select = "SELECT src FROM images JOIN account ON account.id=images.id AND account.id={}".format(id)
        if limit:
            select += " LIMIT {}".format(limit)
        print(select)
        cursor.execute(select)
        res = cursor.fetchall()
        photos = []
        if res:
            for i in res:
                photos.append(i[0])
        else:
            photos.append('default.jpg')
        cursor.close()
        return photos
    return None

def get_user_tags(id=None):
    cursor = db.connection.cursor()
    if id:
        select = "SELECT title FROM tags JOIN user_tag ON user_tag.tg_id=tags.tg_id JOIN account ON account.id=user_tag.us_id AND account.id={}".format(id)
        cursor.execute(select)
    else:
        cursor.execute("SELECT title FROM tags")
    tags = []
    tg = cursor.fetchall()
    for i in tg:
        tags.append(i[0])
    return tags



