from flask import Flask, request, jsonify, render_template
# Importa o módulo Flask e algumas funções úteis:
# - Flask: a classe principal para criar uma aplicação Flask.
# - request: para acessar dados da requisição HTTP.
# - jsonify: para converter dados Python em JSON.
# - render_template: para renderizar arquivos HTML.

from downloader import download_video
# Importa a função download_video do módulo downloader.py.

import os
# Importa o módulo os, que fornece funções para interagir com o sistema operacional.

app = Flask(__name__)
# Cria uma instância da classe Flask. O nome da aplicação é passado como argumento.
# "__name__" é uma convenção que indica o nome do módulo atual. Flask usa isso para determinar o local dos arquivos e recursos.

@app.route('/')
# Define uma rota (endpoint) para a URL raiz ('/'). Quando um usuário acessa a URL raiz do servidor, a função index() será chamada.
def index():
    return render_template('index.html')
    # Renderiza o arquivo 'index.html' localizado na pasta 'templates'.
    # Flask procura automaticamente por arquivos HTML na pasta 'templates'.

@app.route('/download', methods=['POST'])
# Define uma rota para a URL '/download' que aceita apenas requisições POST.
def download():
    data = request.get_json()
    # Acessa os dados JSON enviados na requisição POST e os armazena na variável 'data'.
    url = data['url']
    # Extrai o valor da chave 'url' do JSON recebido.
    path = 'downloads/'
    # Define o caminho onde os vídeos serão salvos.
    if not os.path.exists(path):
        os.makedirs(path)
        # Verifica se a pasta 'downloads' existe. Se não, cria a pasta.
    title = download_video(url, path)
    # Chama a função download_video com a URL e o caminho como argumentos.
    # A função baixa o vídeo e retorna o título do vídeo.
    return jsonify({'message': f'Video "{title}" has been downloaded successfully!'})
    # Retorna uma resposta JSON com uma mensagem de sucesso contendo o título do vídeo baixado.

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    app.run(debug=True)
    # Inicia o servidor Flask.
    # 'debug=True' ativa o modo de depuração, que fornece informações detalhadas sobre erros e reinicia o servidor automaticamente quando o código é alterado.
