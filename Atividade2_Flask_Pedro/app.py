from flask import Flask, render_template
from Controllers import routes
from Models.database import db
import os

app = Flask(__name__,template_folder='Views')

routes.init_app(app)

dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'Models/cards.sqlite3')

if __name__ == '__main__':
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run(host='localhost',port=4000,debug=True)