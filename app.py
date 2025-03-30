from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

@app.route('/')
def home():
    return "YouTube Transcript API is running."

@app.route('/transcript')
def transcript():
    url = request.args.get('url')
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid video URL'}), 400
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item['text'] for item in transcript])
        return jsonify({'transcript': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
