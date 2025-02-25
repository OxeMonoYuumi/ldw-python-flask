from flask import render_template, request, redirect, url_for

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