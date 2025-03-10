import urllib.request
from flask import render_template, request, redirect, url_for
import urllib
import json


Players = []

playerlist = [{'nome':'Vanderlei',
               'comandante':'Rei Ceifador',
               'cores_deck':'Azul,Preto,Branco,Verde e Vermelho'}]


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/players', methods=['GET','POST'])
    def players():
        if request.method == 'POST':
            if request.form.get('player'):
                Players.append(request.form.get('player'))
                return redirect(url_for('players'))
        return render_template('players.html', Players=Players)
    
    @app.route('/cadplayers', methods=['GET','POST'])
    def cadPlayers():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            playerlist.append(form_data)
            return redirect(url_for('cadPlayers'))
        return render_template('cadPlayers.html', playerlist=playerlist)
    
    @app.route('/apimagic', methods=['GET','POST'])
    # @app.route('apimagic/<int:id>', methods=['GET','POST'])
    # def apiMagic(id=None):
    def apiMagic():
        url = 'https://api.magicthegathering.io/v1/cards'
        res = urllib.request.urlopen(url)
        data = res.read()
        cardsjs = json.loads(data)
        # if id:
        #     cinfo=[]
        #     for c in cardsjs:
        #         if c['multiverseid'] == id:
        #             cinfo = c
        #             break
            # if cinfo:
            #     return render_template('apiMagic.html', cinfo=cinfo)
            # else:
            #     return f'Carta com a ID {id} não foi encontrada'
        
        return render_template('apiMagic.html', cardsjs=cardsjs)