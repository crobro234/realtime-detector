from flask import Flask, request
from flask_cors import CORS
import subprocess
import sys
import importlib.util
import os
import json
import time
import shutil

from frame_extractor import extract_frames

app = Flask(__name__)
CORS(app)

def ensure_yt_dlp_installed():
    if importlib.util.find_spec("yt_dlp") is None:
        print("yt-dlp가 설치되어 있지 않아 설치를 시작합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    else:
        print("yt-dlp는 이미 설치되어 있습니다.")

def download_youtube_video(url):
    if not url:
        print("URL이 비어 있습니다.")
        return

    command = [
        "yt-dlp",
        "-f", "best",
        "-o", "video.%(ext)s",
        url
    ]

    try:
        print(f"다운로드 시작: {url}")
        subprocess.run(command, check=True)
        print("✅ 다운로드가 완료되었습니다.")
    except subprocess.CalledProcessError:
        print("❌ 다운로드 중 오류가 발생했습니다.")

@app.route('/receive-url', methods=['POST'])
def receive_url():
    data = request.get_json()
    url = data.get('url')
    print(f"받은 유튜브 URL: {url}")

    start_time = time.time()

    # 1. 영상 다운로드
    download_youtube_video(url)

    # 2. 영상 파일 탐색
    video_file = next((f for f in os.listdir() if f.startswith("video") and f.endswith(('.mp4', '.mkv'))), None)

    if video_file:
        try:
            # 3. 프레임 추출
            extract_frames(video_file, output_dir="frames", interval_sec=2)

            # 4. 누드 감지 실행
            subprocess.run([sys.executable, "check.py", "frames", str(start_time)], check=True)

        finally:
            # ✅ 원본 영상 삭제
            if os.path.exists(video_file):
                os.remove(video_file)
                print(f"🗑️ 원본 영상 삭제됨: {video_file}")

            # ✅ 프레임 폴더 삭제
            if os.path.exists("frames"):
                shutil.rmtree("frames")
                print("🧹 프레임 디렉토리 삭제됨: frames")
    else:
        print("❌ 다운로드된 영상 파일을 찾을 수 없습니다.")

    return {'status': 'success'}

@app.route('/status', methods=['GET'])
def status():
    try:
        with open("result/report.json", "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print("⚠️ 상태 확인 중 오류:", e)
        return {"nudity_detected": False}

if __name__ == '__main__':
    ensure_yt_dlp_installed()
    app.run(port=5000)
