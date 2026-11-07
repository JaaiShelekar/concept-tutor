from gtts import gTTS
from io import BytesIO

def make_audio(text):
    buffer = BytesIO()
    gTTS(text=text[:4500], lang="en").write_to_fp(buffer)
    buffer.seek(0)
    return buffer.read()
