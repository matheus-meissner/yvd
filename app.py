from pytube import YouTube
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

def get_video_download_url(url):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    return yt.title, ys.url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']

    # Supondo que você tenha uma função get_video_download_url que retorna o título e URL de download
    title, download_url = get_video_download_url(url)

    message = f'<span class=\'txt_vermelho\'>Video</span><span class=\'txt_laranja\'>"{title}"</span> foi baixado <span class=\'txt_ciano\'>com sucesso!</span>'
    return jsonify({'message': message, 'download_url': download_url})

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