from pytube import YouTube
from flask import Flask, request, jsonify, render_template, send_from_directory, logging
import os

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Definir nível de log para DEBUG

def download_video(url, path):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    download_path = ys.download(path)
    return yt.title, download_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data['url']

        # Use um diretório temporário para downloads
        download_path = 'downloads'

        # Certifique-se de que o diretório de downloads exista
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Supondo que você tenha uma função download_video que baixa o vídeo e retorna o título e caminho
        title, full_download_path = download_video(url, download_path)

        # Obtenha o nome do arquivo a partir do caminho completo
        filename = os.path.basename(full_download_path)

        # Construir a URL de download
        download_url = request.host_url + 'download_file/' + filename

        message = f'<span class=\'txt_vermelho\'>Video</span><span class=\'txt_laranja\'>"{title}"</span> foi baixado <span class=\'txt_ciano\'>com sucesso!</span>'
        return jsonify({'message': message, 'download_url': download_url})
    except Exception as e:
        app.logger.error(f'Error processing download request: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    try:
        download_path = 'downloads'
        return send_from_directory(download_path, filename, as_attachment=True)
    except Exception as e:
        app.logger.error(f'Error serving file: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/get_thumbnail', methods=['POST'])
def get_thumbnail():
    try:
        data = request.get_json()
        url = data['url']
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        return jsonify({'thumbnail_url': thumbnail_url})
    except Exception as e:
        app.logger.error(f'Error processing thumbnail request: {e}')
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    app.run(debug=True)