from flask import Flask, render_template
# Criando a instância do Flask na variável app
app = Flask(__name__,template_folder='views') # Representa o nome do arquivo que será executado

# Criando a primeira rota da aplicação
@app.route('/') # o @ é o decorator e faz uma ligação da função que está abaixo dele, ao usuário acessar uma rota

# View Function, função de visualização
def home():
    return render_template('index.html')

@app.route('/games')
def game():
    return render_template('games.html')

# Iniciar o servidor
if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)