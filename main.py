import functions_framework
import yt_dlp
import os
import tempfile
import glob
from flask import send_file, jsonify, request
from audio_convert import downgrade_sample_rate
from groq_speech2txt import groq_transcribe
import time

class MyLogger(object):
    def debug(self, msg):
        self.log(msg)
    def warning(self, msg):
        self.log(msg)
    def error(self, msg):
        self.log(msg)
    def log(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8')
        print(msg)

def download_video(url, download_path):
    URLS = [url]
    ydl_opts = {
        'format': 'worstaudio/worst',
        'no_warnings': True,
        'quiet': True,
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'logger': MyLogger()
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
    return error_code

@functions_framework.http
def hello_http(request):
    start_time = time.time()
    time_stats = {}

    # Get the YouTube URL from the request
    request_json = request.get_json(silent=True)
    if request_json and 'url' in request_json:
        youtube_url = request_json['url']
    else:
        youtube_url = request.args.get('url')
    if not youtube_url:
        return jsonify({'error': 'No YouTube URL provided'}), 400

    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download the audio
            download_start = time.time()
            error_code = download_video(youtube_url, temp_dir)
            download_end = time.time()
            time_stats['download_time'] = download_end - download_start
            
            if error_code != 0:
                return jsonify({'error': 'Failed to download audio', 'time_stats': time_stats}), 500

            # Find the downloaded file
            files = os.listdir(temp_dir)
            inputfile = files[0]
            outputfile = f"{inputfile[0:-4]}.mp3"

            # Downgrade sample rate
            conversion_start = time.time()
            downgrade_sample_rate(temp_dir + f"/{inputfile}", temp_dir + f"/{outputfile}")
            conversion_end = time.time()
            time_stats['conversion_time'] = conversion_end - conversion_start

            # Transcribe
            transcription_start = time.time()
            transcription_result = groq_transcribe(temp_dir + f"/{outputfile}")
            transcription_end = time.time()
            time_stats['transcription_time'] = transcription_end - transcription_start

            # Calculate total time
            total_time = time.time() - start_time
            time_stats['total_time'] = total_time

            # Combine results
            combined_result = {
                'transcription': transcription_result,
                'time_stats': time_stats
            }

            return jsonify(combined_result)

    except Exception as e:
        end_time = time.time()
        time_stats['total_time'] = end_time - start_time
        return jsonify({'error': str(e), 'time_stats': time_stats}), 500