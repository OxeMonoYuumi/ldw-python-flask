import pymysql
import pymysql.cursors
from controllers import routes
from flask import Flask, render_template
from models.database import db
import os 

app = Flask(__name__,template_folder='views')
routes.init_app(app)

DB_NAME = 'cards_show'
app.config['DATABASE_NAME'] = DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'
app.config['SECRET_KEY'] = 'cardsecret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



if __name__ == '__main__':
    connection = pymysql.connect(host='localhost',user='root',password='',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"O banco de dados está criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        connection.close()
    
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run(host='localhost',port=4000,debug=True)