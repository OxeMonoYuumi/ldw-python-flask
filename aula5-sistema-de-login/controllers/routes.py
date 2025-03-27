import urllib.request
from flask import render_template, request, redirect, url_for, flash
# Importando o Model
from models.database import db,Game,User
# Esta biblioteca serve para ler uma determinada URL
import urllib
# Converçor de dados para formato JSON
import json
# Importando biblioteca para Hash de senha
from werkzeug.security import generate_password_hash,check_password_hash
# Importando edição de Flash Message
from markupsafe import Markup # Inclui HTML dentro das Flash messages

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
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            # Selecionando o jogo no banco para ser excluído
            game = Game.query.get(id)
            # Deletar o game do banco pela ID
            db.session.delete(game)
            db.session.commit()
            
        if request.method == 'POST':
            # Cadastra um novo jogo
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'], request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            # Envia os valores para o banco
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        else:
            # Paginação
            # A variável abaixo captura o valor de 'page' que foi passado pelo método GET. Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # valor padrão definido por página, definido como 5
            per_page = 5
            # Está sendo feito um select no banco a partir da página informada (page) e filtrando os registro de 5 em 5 (per_page)
            games_page = Game.query.paginate(page=page, per_page=per_page)
            return render_template('estoque.html', gamesestoque=games_page)
            
            # Método do SQLAlchemy que faz um select geral no banco na tabela Games
            # gamesestoque = Game.query.all()
            # return render_template('estoque.html', gamesestoque=gamesestoque)
        
    @app.route('/edit/<int:id>', methods=['GET','POST'])
    def edit(id):
        # Buscando informações do jogo
        game = Game.query.get(id)
        # Vai Editar o jogo com as informações do formulário
        if request.method == 'POST':
            game.titulo = request.form['titulo']
            game.ano = request.form['ano']
            game.categoria = request.form['categoria']
            game.plataforma = request.form['plataforma']
            game.preco = request.form['preco']
            game.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editgame.html', game=game)
    
    # Rota de Login
    @app.route('/login', methods=['GET','POST'])
    def login():
        return render_template('login.html')
    
    # Rota de Cadastro
    @app.route('/caduser', methods=['GET','POST'])
    def caduser():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            # verifica se o usuário
            user = User.query.filter_by(email=email).first()
            
            # se o usuario existir
            if user:
                msg = Markup("Usuário já cadastrado <a href='/login'>Login</a>")
                flash(msg, 'danger')
                return redirect(url_for('caduser'))
            # Caso o usuario não exista
            else:
                # Gerando o hash
                hashed_password = generate_password_hash(password, method='scrypt')
                new_user = User(email=email,password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                # Redirecionando para página de login
                return redirect(url_for('login'))
        return render_template('caduser.html')