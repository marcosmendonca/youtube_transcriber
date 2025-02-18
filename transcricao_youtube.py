from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def get_transcription(video_url):
    try:
        video_id = re.search(r"v=([\w-]+)", video_url).group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
        text = "\n".join([t['text'] for t in transcript])
        return text
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Transcrição de Vídeo</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h2>Insira o link do vídeo do YouTube:</h2>
        <input type="text" id="video_url" placeholder="Cole o link aqui">
        <button onclick="transcribe()">Transcrever</button>
        <h3>Transcrição:</h3>
        <pre id="transcription"></pre>
        
        <script>
            function transcribe() {
                let video_url = document.getElementById('video_url').value;
                fetch('/transcribe', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({video_url: video_url})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('transcription').innerText = data.transcription;
                })
                .catch(error => console.error('Erro:', error));
            }
        </script>
    </body>
    </html>
    '''

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    video_url = data.get('video_url')
    transcription = get_transcription(video_url)
    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Render usa portas acima de 5000
    app.run(host="0.0.0.0", port=port, debug=True)


