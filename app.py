from flask import Flask, request, jsonify, render_template, after_this_request
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app, origins=["https://yvd.vercel.app"])  # Habilitar CORS para o front-end na Vercel

def get_video_url(url):
    yt = YouTube(url)
    video_url = yt.streams.get_highest_resolution().url  # Pegue a URL direta do stream
    print("Video URL:", video_url)  # Log para verificar a URL
    return yt.title, video_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data['url']
        title, video_url = get_video_url(url)  # Obtenha a URL do vídeo
        
        # Retorne apenas o link direto para o front-end
        return jsonify({"download_url": video_url, "message": f"Video '{title}' pronto para download."})

    except Exception as e:
        print(f"Erro ao processar o download: {e}")
        return jsonify({"error": "Falha ao processar o download"}), 500

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
