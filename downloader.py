from pytube import YouTube

def download_video(url, path): #cria função de download;
    yt = YouTube(url) #atribuiçao de variáveis: link;
    ys = yt.streams.get_highest_resolution() #seleciona a maior qualidade disponível;
    ys.download(path) #faz o download no caminho especificado;
    return yt.title #retorna o título do vídeo;

# # Bloco de teste
# if __name__ == "__main__":
#     test_url = "https://www.youtube.com/watch?v=E8E_LklsJw0"
#     download_path = "C:\\Users\\matheus_meissner\\Desktop\\atma\\teste_flask"  # Certifique-se de que esta pasta exista ou crie-a
#     title = download_video(test_url, download_path)
#     print(f'Downloaded video title: {title}')