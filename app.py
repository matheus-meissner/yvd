from flask import Flask, request, jsonify, render_template
from downloader import download_video
import os

app = Flask(__name__)

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
    message = f'<span class=\'txt_vermelho\'>Video</span><span class=\'txt_laranja\'>"{title}"</span> has been downloaded <span class=\'txt_ciano\'>successfully!'
    return jsonify({'message': message})

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    app.run(debug=True)
