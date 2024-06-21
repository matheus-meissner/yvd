from pytube import YouTube
from io import BytesIO
from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)

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
    url = data['url']
    
    title, buffer = download_video(url)
    return send_file(buffer, as_attachment=True, download_name=f"{title}.mp4", mimetype='video/mp4')

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
