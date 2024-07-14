import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
print(f"groq api key: {groq_api_key}")

def groq_transcribe(filename):
    client = Groq(api_key=groq_api_key)
    filename = filename
    print(f"groq: {filename}")

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # json or verbose_json
            language="zh",  # Optional
            temperature=0.0  # Optional
        )
        return transcription.text

if __name__ == "__main__":
    print(groq_transcribe('方脸说：中国爆出油罐车混装事件，中国食品安全问题为何如此严重？特供食品丨中国食品监管体系.mp3'))