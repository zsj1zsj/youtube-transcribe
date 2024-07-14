import yt_dlp
import os
import logging

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
    'format': 'm4a/worstaudio/worst',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        }],
    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    'logger': MyLogger()
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
    return error_code

def extract_info(url):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {
           'quiet': True,  # Suppress output
           'simulate': True,  # Do not download the video
       }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # ℹ️ ydl.sanitize_info makes the info json-serializable
        return info['title']
    
if __name__ == "__main__":
    print(extract_info('https://www.youtube.com/watch?v=i3sR83xEa9M'))
