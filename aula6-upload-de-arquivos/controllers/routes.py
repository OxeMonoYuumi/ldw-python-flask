import urllib.request
from flask import render_template, request, redirect, url_for, flash, session
from markupsafe import Markup # Inclui HTML dentro das Flash messages
from models.database import db,Card
import urllib
import os
import uuid
import json

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')
    @app.route('/gallery', methods=['GET','POST'])
    def gallery():
        images = Card.query.all()
        return render_template('gallery.html', images=images)
    
    FILE_TYPES = set(['png','jpg','jpeg','gif'])
    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in FILE_TYPES
    @app.route('/cadcard', methods=['GET','POST'])
    def cadcard():
        if request.method == 'POST':
            name = request.form['name']
            collection = request.form['collection']
            image = request.files['image']
            if not arquivos_permitidos(image.filename):
                return redirect(request.url)
            filename = str(uuid.uuid4())
            new_card=Card(name=name,image=filename,collection=collection)
            db.session.add(new_card)
            db.session.commit()
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            flash("Carta cadastrada com sucesso", 'success')
        return render_template('cadcard.html')