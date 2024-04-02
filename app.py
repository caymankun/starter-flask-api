from flask import Flask, request, Response
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('video_url')
    if not video_url:
        return '動画のURLが提供されていません', 400
    
    try:
        # yt-dlpコマンドを実行して動画をダウンロード
        command = ["yt-dlp", "-o", "-", "--format", "best", video_url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # yt-dlpの出力をそのままブラウザに出力
        return Response(result.stdout, mimetype='video/mp4')
    except subprocess.CalledProcessError as e:
        return f'エラーが発生しました: {str(e)}', 500

@app.route('/download_audio', methods=['GET'])
def download_audio():
    video_url = request.args.get('video_url')
    if not video_url:
        return '動画のURLが提供されていません', 400
    
    try:
        # yt-dlpコマンドを実行して音楽をダウンロード
        command = ["yt-dlp", "-o", "-", "--extract-audio", "--audio-format", "mp3", video_url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # yt-dlpの出力をそのままブラウザに出力
        return Response(result.stdout, mimetype='audio/mpeg')
    except subprocess.CalledProcessError as e:
        return f'エラーが発生しました: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
