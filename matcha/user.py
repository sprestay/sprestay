from app import db
from functions import get_age, haversine
from flask import session
import re

class User(object):
    def __init__(self, id=-1, username='', first_name='', second_name='', gender='m', birth='', age=0, orient='bi', bio='', coords=[], last_seen='', fame=0, manually=0, photo="default.jpg", common_tag=0):
      self.id = id
      self.username = username
      self.first_name = first_name
      self.second_name = second_name
      self.gender = gender
      self.birth = birth
      self.age = age
      self.orient = orient
      self.bio = bio
      if ('username' in session and session['username'] != self.username):
        cursor = db.connection.cursor()
        cursor.execute("SELECT X, Y FROM account WHERE username=%s",(session['username'],))
        res = cursor.fetchall()[0]
        self.distance = haversine(coords[0], coords[1], res[0], res[1])
      else:
        self.distance = 0
      self.coords = coords
      self.last_seen = last_seen
      self.fame = fame
      self.manually = manually
      self.photo = photo
      self.common_tag = common_tag
      self.clever = 5 * self.common_tag + 2 * self.fame - 10 * self.distance

    @classmethod
    def get_filter(cls, **kwargs):
      cursor = db.connection.cursor()
      search = ""
      if kwargs:
        key = list(kwargs.keys())
        i = 0
        while i < len(kwargs): #Передаем в ключе словаря условие поиска (age<) isalpha проверяем есть ли условие
          if i == 0:
            search += " WHERE " + key[0] + "='" + str(kwargs[key[0]]) + "'" 
          else:
            if not re.search(r'fame<', key[i]) and not re.search(r'fame>', key[i]) and not key[i] == "JUST_ADD": #фильтр по популярности
              search += " AND " + key[i] + "='" + str(kwargs[key[i]]) + "'"
            elif key[i] == "JUST_ADD": # условие костыль для пользовательских запросов
              search += str(kwargs[key[i]])
            else:
              search += " AND " + key[i].replace("s", "") + "=" + str(kwargs[key[i]]) #костыль для того чтобы в словаре не было одинаковых ключей
          i += 1
      select = "SELECT id, username, first_name, second_name, gender, birth, orient, bio, X, Y, last_seen, fame, manually FROM account" + search
      cursor.execute(select)
      res = cursor.fetchall()
      users = []
      for i in res:
          cursor.execute("SELECT src FROM images WHERE id=%s LIMIT 1", (i[0], ))
          res = cursor.fetchone()
          if res:
            photo = res[0]
          else:
            photo = "default.jpg"
          users.append(cls(id=i[0], username=i[1], first_name=i[2], second_name=i[3], gender=i[4], birth=i[5], age=get_age(i[5]), orient=i[6], bio=i[7], coords=[i[8],i[9]], last_seen=i[10], fame=i[11], manually=i[12], photo=photo))
      cursor.close()
      return users

    def update(self, **kwargs):
      cursor = db.connection.cursor()
      update_str = "UPDATE account SET "
      i = 0
      key = list(kwargs.keys())
      while i < len(key):
        if i != len(key) - 1:
          update_str += key[i] + "='" + str(kwargs[key[i]]) + "', "
        else:
          update_str += key[i] + "='" + str(kwargs[key[i]]) + "' " #лишняя запятая
        i += 1
      update_str += "WHERE id='" + str(self.id) + "'"
      cursor.execute(update_str)
      db.connection.commit()
      cursor.close()

    def __str__(self):
      return ("Username: {}".format(self.username))
