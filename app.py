from pytube import YouTube
from flask import Flask, request, send_file, render_template
import os
import tempfile

app = Flask(__name__)

def download_video(url):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    ys.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))
    return yt.title, temp_file.name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']

    # Supondo que você tenha uma função download_video que baixa o vídeo e retorna o título e caminho
    title, full_download_path = download_video(url)

    # Enviar o arquivo como um download para o cliente
    return send_file(full_download_path, as_attachment=True, download_name=f"{title}.mp4")

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