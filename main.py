# Imports
from IPython import display as ipd
from audiocraft.models import musicgen
import torchaudio
import os

from pydub import AudioSegment

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


# Function to convert WAV to MP3
def wav_to_mp3(wav_file, mp3_file):
    try:
        print("Starting conversion...")
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")  # No await needed
        print("Conversion completed!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def genrate_music(genre, duration, mood, tempo):
        prompt = f"{mood}, {genre}, at {tempo} BPM" #Prompt Construction

        model.set_generation_params(duration=int(duration)) # Ai model configuration
        res = model.generate([prompt], progress=True)
        
        #Save the audio files
        for i, audio in enumerate(res):
            audio_cpu = audio.cpu()
            file_path = os.path.join(output_dir, f"audio.wav")
            torchaudio.save(file_path, audio_cpu, sample_rate=32000)

            # Use correct file path that matches your saved file
            wav_to_mp3("Output/audio.wav", "Output/audio.mp3")  # Convert to MP3


    



# Handelr for HTTP requests for bridge between frontend and backend
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # CORS headers to allow frontend requests
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # Handle OPTIONS requests for CORS preflight
    def do_OPTIONS(self):
        self._set_headers()

    # Handle POST requests
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        genre = data.get('genre', '')
        duration = data.get('duration', 10)
        mood = data.get('mood', '')
        tempo = data.get('tempo', '')

        print(f"Received input: {genre}, {duration}, {mood}, {tempo}")

        genrate_music(genre, duration, mood, tempo) # Initiate music generation

        response = {"result": f"ready"} # Respond back to frontend
        response_bytes = json.dumps(response).encode('utf-8')

        self._set_headers()
        self.wfile.write(response_bytes)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server at http://localhost:{port}')

    try:
        os.startfile("index.html") # Start the front end HTML file
    except FileNotFoundError:
        print("index.html not found. Please ensure the file exists in the current directory.")

    httpd.serve_forever() #Start the server

# Define the output directory
output_dir = r'Output'
model = musicgen.MusicGen.get_pretrained('facebook/musicgen-small', device='cuda')


run() # Start program
