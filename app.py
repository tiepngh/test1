import yt_dlp as youtube_dl  # Import yt-dlp thay vì youtube_dl
from flask import Flask, render_template, request, send_file, jsonify
from pydub import AudioSegment
import os
import tempfile
import shutil

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                # Xử lý video và chuyển thành MP3
                filename = download_video(url)
                mp3_file = convert_to_mp3(filename)
                return send_file(mp3_file, as_attachment=True)
            except Exception as e:
                return jsonify({"error": str(e)}), 500  # Trả về lỗi nếu có ngoại lệ
    return render_template('index.html')

def download_video(url):
    # Cấu hình yt-dlp để tải video và trích xuất âm thanh
    ydl_opts = {
        'format': 'bestaudio/best',  # Chọn định dạng âm thanh tốt nhất
        'outtmpl': tempfile.mktemp(prefix='downloads/', suffix='.webm'),  # Lưu trữ tạm thời
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(result)
            return filename
    except Exception as e:
        raise Exception(f"Error downloading video: {e}")

def convert_to_mp3(filename):
    try:
        # Tạo thư mục tạm thời cho file chuyển đổi
        temp_dir = tempfile.mkdtemp()

        # Dùng pydub để đảm bảo âm thanh ở bitrate 128kbps
        audio = AudioSegment.from_file(filename)
        mp3_file = os.path.join(temp_dir, f"converted_{os.path.basename(filename)}.mp3")
        
        # Chuyển đổi sang MP3
        audio.export(mp3_file, format="mp3", bitrate="128k")
        os.remove(filename)  # Xóa file gốc sau khi chuyển đổi

        # Xóa thư mục tạm sau khi sử dụng
        shutil.rmtree(temp_dir)
        
        return mp3_file
    except Exception as e:
        raise Exception(f"Error converting to MP3: {e}")

if __name__ == '__main__':
    app.run(debug=True)
