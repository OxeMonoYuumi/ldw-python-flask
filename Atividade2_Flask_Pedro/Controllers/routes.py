import urllib.request
from flask import render_template, request, redirect, url_for
from Models.database import db,Cards
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

    @app.route('/cardestoque', methods=['GET','POST'])
    @app.route('/cardestoque/delete/<int:id>')
    def cardEstoque(id=None):
        if id:
            card = Cards.query.get(id)
            db.session.delete(card)
            db.session.commit()

        if request.method == 'POST':
            newCard = Cards(request.form['name'],request.form['type'],request.form['color'],request.form['rarity'],request.form['qtd'],request.form['collection'])
            db.session.add(newCard)
            db.session.commit()
            return redirect(url_for('cardEstoque'))
        else:
            page = request.args.get('page',1, type=int)
            per_page = 5
            cards_page = Cards.query.paginate(page=page, per_page=per_page)
            return render_template('cardEstoque.html', cardsEstoque = cards_page)
    
    @app.route('/editCard/<int:id>', methods=['GET','POST'])
    def editcard(id):
        card = Cards.query.get(id)
        if request.method == 'POST':
            card.name = request.form['name']
            card.type = request.form['type']
            card.color = request.form['color']
            card.rarity = request.form['rarity']
            card.qtd = request.form['qtd']
            card.collection = request.form['collection']
            db.session.commit()
            return redirect(url_for('cardEstoque'))
        return render_template('editCard.html', card=card)
            