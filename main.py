from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview-url/<trackId>')
def get_preview_url(trackId):
    try:
        embedUrl = f"https://open.spotify.com/embed/track/{trackId}"
        embedResponse = requests.get(embedUrl)
        embedText = embedResponse.text
        previewUrl = embedText.split('"audioPreview":{"url":')[1].split('"},"hasVideo"')[0]
        return jsonify({'previewUrl': previewUrl})
    except Exception as e:
        print('Error fetching preview URL:', e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/data/<path:filename>')
def data_files(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(debug=False)
