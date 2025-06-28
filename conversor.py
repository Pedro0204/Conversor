import streamlit as st
from yt_dlp import YoutubeDL

# Função para baixar o vídeo com a qualidade selecionada
def download_video(url, quality):
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',  # Baixar vídeo até a qualidade selecionada
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Diretório e nome do arquivo
        'merge_output_format': 'mp4',  # Mesclar vídeo e áudio em MP4
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Função para baixar somente o áudio
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Pode alterar para outro formato, como 'wav'
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Interface do Streamlit
st.title("Video/Audio Downloader")

video_url = st.text_input("Digite a URL do vídeo (YouTube, X, etc.)", "")

# Adicionar uma opção de escolha entre vídeo e áudio
download_type = st.radio("Escolha o tipo de download", ("Vídeo Completo", "Somente Áudio"))

# Adicionar uma opção para escolher a qualidade do vídeo (se a opção de vídeo for selecionada)
if download_type == "Vídeo Completo":
    quality = st.selectbox("Escolha a qualidade máxima do vídeo", options=["1080p", "720p", "480p", "360p", "Qualidade máxima"])

# Mapeando as resoluções para os valores numéricos
quality_map = {
    "1080p": 1080,
    "720p": 720,
    "480p": 480,
    "360p": 360,
    "Qualidade máxima": "",  # Para obter a melhor qualidade disponível
}

if st.button("Baixar"):
    if video_url:
        try:
            if download_type == "Vídeo Completo":
                st.write("Baixando vídeo...")
                download_video(video_url, quality_map[quality])
                st.success("Download de vídeo e áudio concluído!")
            else:
                st.write("Baixando áudio...")
                download_audio(video_url)
                st.success("Download de áudio concluído!")
        except Exception as e:
            st.error(f"Erro ao baixar o {download_type.lower()}: {e}")
    else:
        st.warning("Por favor, insira uma URL válida.")
