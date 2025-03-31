import yt_dlp as youtube_dl  # Import yt-dlp thay vì youtube_dl
from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            # Xử lý video và chuyển thành MP3
            filename = download_video(url)
            mp3_file = convert_to_mp3(filename)
            return send_file(mp3_file, as_attachment=True)
    return render_template('index.html')

def download_video(url):
    # Cấu hình yt-dlp để tải video và trích xuất âm thanh
    ydl_opts = {
        'format': 'bestaudio/best',  # Chọn định dạng âm thanh tốt nhất
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Lưu trữ video vào thư mục downloads
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        filename = f"downloads/{result['id']}.webm"  # Sử dụng định dạng webm để tải âm thanh
    return filename

def convert_to_mp3(filename):
    # Dùng pydub để đảm bảo âm thanh ở bitrate 128kbps
    audio = AudioSegment.from_file(filename)
    mp3_file = f"downloads/converted_{os.path.basename(filename)}.mp3"
    audio.export(mp3_file, format="mp3", bitrate="128k")
    os.remove(filename)  # Xóa file gốc sau khi chuyển đổi
    return mp3_file

if __name__ == '__main__':
    app.run(debug=True)
