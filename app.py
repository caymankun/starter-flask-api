from flask import Flask, request, send_file, jsonify
from yt_dlp import YoutubeDL
import subprocess

app = Flask(__name__)

@app.route('/v', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': '動画のURLが提供されていません'}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return send_file(filename, as_attachment=True)
        except Exception as e:
            print('動画のダウンロードに失敗しました:', str(e))
            return jsonify({'error': '動画のダウンロードに失敗しました'}), 500

@app.route('/a', methods=['GET'])
def download_audio():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': '動画のURLが提供されていません'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            mp3_filename = filename.split('.')[0] + '.mp3'
            # ffmpegを使用して音声をMP3に変換
            subprocess.run(['ffmpeg', '-i', filename, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', mp3_filename], capture_output=True)
            return send_file(mp3_filename, as_attachment=True)
        except Exception as e:
            print('音楽のダウンロードに失敗しました:', str(e))
            return jsonify({'error': '音楽のダウンロードに失敗しました'}), 500
            
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
