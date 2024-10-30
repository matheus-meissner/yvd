from flask import Flask, request, jsonify, render_template, send_file, after_this_request
from flask_cors import CORS  # Importe o CORS
import os
from pytube import YouTube

app = Flask(__name__)
CORS(app, origins=["https://yvd.vercel.app"])  # Adicione o CORS ao seu app Flask

def download_video(url, path):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution().url
    print(ys)
    video_path = ys.download(path)
    return yt.title, video_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])


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
