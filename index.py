from pytube import YouTube
import os
import tempfile
from flask import Flask, request, jsonify, render_template

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

    # Use a temporary directory for downloads
    with tempfile.TemporaryDirectory() as download_path:
        title = download_video(url, download_path)
        # Path to the downloaded video file
        downloaded_file = os.path.join(download_path, os.listdir(download_path)[0])

        with open(downloaded_file, 'rb') as file:
            content = file.read()

    # Return the video file as a response
    response = app.response_class(
        response=content,
        status=200,
        mimetype='application/octet-stream'
    )
    response.headers.set('Content-Disposition', 'attachment', filename=f'{title}.mp4')

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
    app.run(debug=True)
