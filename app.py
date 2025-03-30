from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import urllib.parse

app = Flask(__name__)

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

@app.route('/transcript')
def transcript():
    url = request.args.get('url')
    cookie_raw = request.args.get('cookie')  # URL-decoded automatically
    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({'error': 'Invalid video URL'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            cookies={"Cookie": cookie_raw} if cookie_raw else None
        )
        text = " ".join([item['text'] for item in transcript])
        return jsonify({'transcript': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
