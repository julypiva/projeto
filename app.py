from flask import Flask, render_template, request
from selenium_script import iniciar_monitoramento
from analise_sentimento import processar_analise_sentimento

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    mensagem = ""
    resultados_sentimento = []

    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        perfil = request.form['perfil']

        # Executando o monitoramento
        mensagem = iniciar_monitoramento(usuario, senha, perfil)

        # Após o monitoramento, processa a análise de sentimentos
        resultados_sentimento = processar_analise_sentimento()

    return render_template('index.html', mensagem=mensagem, resultados_sentimento=resultados_sentimento)

@app.route('/estatistica')
def estatistica():
    return render_template('estatistica.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    app.run(debug=True)

