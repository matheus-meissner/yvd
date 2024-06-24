import io
from pytube import YouTube
from flask import Flask, request, jsonify, render_template, send_file
import os

app = Flask(__name__)

def download_video(url):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()

    # Baixar o vídeo para um buffer em memória
    buffer = io.BytesIO()
    ys.stream_to_buffer(buffer)
    buffer.seek(0)

    return yt.title, buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']

    # Baixar o vídeo para um buffer em memória
    title, video_buffer = download_video(url)

    # Construir a URL de download
    message = f'<span class=\'txt_vermelho\'>Video</span><span class=\'txt_laranja\'>"{title}"</span> foi baixado <span class=\'txt_ciano\'>com sucesso!</span>'
    return jsonify({'message': message, 'title': title})

@app.route('/download_file', methods=['GET'])
def download_file():
    url = request.args.get('url')
    title, video_buffer = download_video(url)
    return send_file(video_buffer, as_attachment=True, download_name=f"{title}.mp4")

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