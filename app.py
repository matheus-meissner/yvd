from flask import Flask, request, jsonify, render_template, send_file, after_this_request
from flask_cors import CORS  # Importe o CORS
import os
from pytube import YouTube

app = Flask(__name__)
CORS(app, origins=["https://yvd.vercel.app"])  # Adicione o CORS ao seu app Flask

def download_video(url, path):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    video_path = ys.download(path)
    return yt.title, video_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    home = os.path.expanduser("~")  # Determinar o caminho de downloads padrão do sistema operacional
    if os.name == 'nt':  # Windows
        download_path = os.path.join(home, 'Downloads')
    else:  # macOS, Linux, etc.
        download_path = os.path.join(home, 'Downloads')
    
    # Certificar que o diretório de downloads existe
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    title, video_path = download_video(url, download_path)

    # Enviar o arquivo como anexo para o navegador fazer o download
    response = send_file(video_path, as_attachment=True, download_name=f"{title}.mp4")

    # Adicionar cabeçalhos para forçar o download
    response.headers["Content-Disposition"] = f"attachment; filename={title}.mp4"
    response.headers["Content-Type"] = "application/octet-stream"
    
    # Adicionar mensagem à resposta
    message = f'<span class=\'txt_vermelho\'>Video</span><span class=\'txt_laranja\'>"{title}"</span> foi baixado <span class=\'txt_ciano\'>com sucesso!</span>'
    response.headers["X-Download-Message"] = message
    
    return response

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
    app.run(debug=False)
