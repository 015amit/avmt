from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY']="hard to guess"
app.config['MYSQL_DATABASE_USER'] = 'b17b8fca64d7e4'
app.config['MYSQL_DATABASE_PASSWORD'] = '737a0163'
app.config['MYSQL_DATABASE_DB'] = 'heroku_0ca59ae2f6a7afa'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'
mysql.init_app(app)
 
conn = mysql.connect()
cursor =conn.cursor()


from school import routes
from school import models