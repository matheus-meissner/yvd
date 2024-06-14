from pytube import YouTube
import os
from flask import Flask, render_template, request, jsonify
from waitress import serve
import logging

app = Flask(__name__)

def download_video(url, path):
    logging.info(f"Starting download for URL: {url}")
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    ys.download(path)
    logging.info(f"Download complete for URL: {url}")
    return yt.title


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']

    logging.info(f"Received download request for URL: {url}")

    download_path = '/tmp'

    logging.info(f"Download path: {download_path}")

    if not os.path.exists(download_path):
        os.makedirs(download_path)
        logging.info(f"Created download directory at: {download_path}")

    title = download_video(url, download_path)

    message = f'<span class="txt_vermelho">Vídeo</span><span class="txt_laranja">{title}</span> foi baixado <span class="txt_ciano">com sucesso!</span>'
    logging.info(f"Download successful: {title}")
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
    serve(app, host='0.0.0.0', port=8080)
