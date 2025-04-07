from flask import Flask, render_template
import pymysql.cursors
from controllers import routes
# Importanto o model
from models.database import db
# Importanto a biblioteca OS (comandos de S.O)
import os
# Importando o PyMySQL
import pymysql

# Criando a instância do Flask na variável app
app = Flask(__name__,template_folder='views') # Representa o nome do arquivo que será executado

routes.init_app(app)

# Permite ler o diretório absoluto de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passando o diretório do banco ao SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

# Define o nome do banco
DB_NAME = 'thegames'
app.config['DATABASE_NAME'] = DB_NAME

# Passando o diretório do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

# Caso o banco tenha senha
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:admin@localhost/{DB_NAME}'

# Secrete para as flash messages
app.config['SECRET_KEY'] = 'thegamessecret'

# Define o tempo de duração da sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Iniciar o servidor
if __name__ == '__main__':
    # Conecta ao MySQL para criar o banco de dados (se não existir)
    connection = pymysql.connect(host='localhost',user='root',password='',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Cria o banco de dados se ele não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"O banco de dados está criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        connection.close()
    
    # Iniciando a aplicação Flask e cria as tabelas do banco
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run(host='localhost',port=5000,debug=True)