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
    path = 'downloads/'
    if not os.path.exists(path):
        os.makedirs(path)
    title = download_video(url, path)
    message = f'Video "<span class=\'txt_vermelho\'>{title}</span>" has been downloaded <span class=\'txt_laranja\'>successfully!</span>'
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
