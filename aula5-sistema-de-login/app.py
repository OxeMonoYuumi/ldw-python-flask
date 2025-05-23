from flask import Flask, render_template
from controllers import routes
# Importanto o model
from models.database import db
# Importanto a biblioteca OS (comandos de S.O)
import os

# Criando a instância do Flask na variável app
app = Flask(__name__,template_folder='views') # Representa o nome do arquivo que será executado

routes.init_app(app)

# Permite ler o diretório absoluto de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passando o diretório do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

# Secrete para as flash messages
app.config['SECRET_KEY'] = 'thegamessecret'

# Define o tempo de duração da sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Iniciar o servidor
if __name__ == '__main__':
    db.init_app(app=app)
    # Cria o banco de dados quando a aplicação é rodada
    with app.test_request_context():
        db.create_all()
    app.run(host='localhost',port=5000,debug=True)