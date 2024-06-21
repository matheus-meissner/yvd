from pytube import YouTube
from io import BytesIO
from flask import Flask, request, jsonify, render_template, send_file
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def download_video(url):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    buffer = BytesIO()
    ys.stream_to_buffer(buffer)
    buffer.seek(0)
    return yt.title, buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    app.logger.debug(f"Request JSON data: {data}")
    url = data.get('url', None)
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    app.logger.debug(f"Downloading video from URL: {url}")
    try:
        title, buffer = download_video(url)
        app.logger.debug(f"Downloaded video: {title}")
        return send_file(buffer, as_attachment=True, download_name=f"{title}.mp4", mimetype='video/mp4')
    except Exception as e:
        app.logger.error(f"Error downloading video: {str(e)}")
        return jsonify({'error': 'Failed to download video'}), 500

@app.route('/get_thumbnail', methods=['POST'])
def get_thumbnail():
    data = request.get_json()
    app.logger.debug(f"Request JSON data: {data}")
    url = data.get('url', None)
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    return jsonify({'thumbnail_url': thumbnail_url})

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=False)
