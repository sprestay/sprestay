from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
import os

app = Flask(__name__)
db = MySQL(app)
socketio = SocketIO(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sprestay'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'matcha'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = './static/photos/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ADDRESANT'] = 'matchat@bk.ru'
app.config['ADDRESANT_PASSWD'] = '2512root2009'

with app.app_context():
    cursor = db.connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS account (id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(20) NOT NULL, first_name VARCHAR(20) NOT NULL, second_name VARCHAR(20) NOT NULL, email VARCHAR(100) NOT NULL,\
    confirm VARCHAR(75), password VARCHAR(100) NOT NULL, gender ENUM('m', 'w'), birth DATE, orient ENUM('hetero','bi','homo'), bio TEXT, X float, Y float, manually BOOLEAN DEFAULT false, last_seen DATETIME DEFAULT CURRENT_TIMESTAMP, fame INT DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS images (id INT, src varchar(100), FOREIGN KEY (id) REFERENCES account (id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tags (tg_id INT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(20))")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_tag (us_id INT, tg_id INT, FOREIGN KEY (us_id) REFERENCES account (id), FOREIGN KEY (tg_id) REFERENCES tags (tg_id) ON DELETE CASCADE)")
    cursor.execute('CREATE TABLE IF NOT EXISTS tmp_email (user_id INT, email VARCHAR(100), confirm VARCHAR(25), FOREIGN KEY (user_id) REFERENCES account (id))')
    cursor.execute("CREATE TABLE IF NOT EXISTS visits (who INT, whom INT, FOREIGN KEY (who) REFERENCES account (id), FOREIGN KEY (whom) REFERENCES account (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS blacklist (who INT, whom INT, FOREIGN KEY (who) REFERENCES account (id), FOREIGN KEY (whom) REFERENCES account (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS likes (who INT, whom INT, FOREIGN KEY (who) REFERENCES account (id), FOREIGN KEY (whom) REFERENCES account (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS reports (who INT, whom INT, FOREIGN KEY (who) REFERENCES account (id), FOREIGN KEY (whom) REFERENCES account (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (who INT, msg TEXT, whom INT, FOREIGN KEY (who) REFERENCES account (id), FOREIGN KEY (whom) REFERENCES account (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS matches (user1 INT, user2 INT, FOREIGN KEY (user1) REFERENCES account (id), FOREIGN KEY (user2) REFERENCES account (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS notifications (who INT, whom INT, type ENUM('checked', 'liked', 'match', 'dislike', 'msg'), FOREIGN KEY (who) REFERENCES account (id), FOREIGN KEY (whom) REFERENCES account (id))")
    db.connect.commit()
    cursor.close()

