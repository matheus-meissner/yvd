from pytube import YouTube
import logging

def download_video(url, path):
    logging.info(f"Starting download for URL: {url}")
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    ys.download(path)
    logging.info(f"Download complete for URL: {url}")
    return yt.title


# # Bloco de teste
# if __name__ == "__main__":
#     test_url = "https://www.youtube.com/watch?v=E8E_LklsJw0"
#     download_path = "C:\\Users\\matheus_meissner\\Desktop\\atma\\teste_flask"  # Certifique-se de que esta pasta exista ou crie-a
#     title = download_video(test_url, download_path)
#     print(f'Downloaded video title: {title}')