from flask import Flask, request, jsonify, render_template
from pytube import YouTube
import os

app = Flask(__name__)

def download_video(url, path):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    ys.download(path)
    return yt.title

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    
    # Determinar o caminho de downloads padrão do sistema operacional
    home = os.path.expanduser("~")
    if os.name == 'nt':  # Windows
        download_path = os.path.join(home, 'Downloads')
    else:  # macOS, Linux, etc.
        download_path = os.path.join(home, 'Downloads')

    # Certificar que o diretório de downloads existe
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # Supondo que você tenha uma função download_video que baixa o vídeo e retorna o título
    title = download_video(url, download_path)
    
    message = f'<span class=\'txt_vermelho\'>Video</span><span class=\'txt_laranja\'>"{title}"</span> has been downloaded <span class=\'txt_ciano\'>successfully!</span>'
    return jsonify({'message': message})

@app.route('/get_thumbnail', methods=['POST'])
def get_thumbnail():
    data = request.get_json()
    url = data['url']
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    return jsonify({'thumbnail_url': thumbnail_url})

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    app.run(debug=True)
