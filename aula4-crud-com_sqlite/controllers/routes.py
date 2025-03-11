import urllib.request
from flask import render_template, request, redirect, url_for
# Importando o Model
from models.database import db,Game
# Esta biblioteca serve para ler uma determinada URL
import urllib
# Converçor de dados para formato JSON
import json

jogadores = []

gameslist= [{'titulo':'CS-GO',
        'ano':2012,
        'categoria':'FPS'}]

def init_app(app):
    # Criando a primeira rota da aplicação
    @app.route('/') # o @ é o decorator e faz uma ligação da função que está abaixo dele, ao usuário acessar uma rota

    # View Function, função de visualização
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET','POST'])
    def game():
        games = gameslist[0]
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('game'))
        return render_template('games.html', games=games,gameslist=gameslist,jogadores=jogadores)

    @app.route('/cadgames', methods=['GET','POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gameslist.append(form_data)
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html', gameslist=gameslist)
    
    @app.route('/apigames', methods=['GET','POST'])
    # Passando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET','POST'])
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        # print(res)
        data = res.read()
        gamesjs = json.loads(data)
        if id:
            ginfo=[]
            for g in gamesjs:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado!'
        
        return render_template('apigames.html', gamesjs=gamesjs)
    
    # Rota com CRUD de jogos
    @app.route('/estoque', methods=['GET','POST'])
    def estoque():
        if request.method == 'POST':
            # Cadastra um novo jogo
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'], request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            # Envia os valores para o banco
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        # Método do SQLAlchemy que faz um select geral no banco na tabela Games
        gamesestoque = Game.query.all()
        return render_template('estoque.html', gamesestoque=gamesestoque)
        