import os
import tempfile

def convert_to_wav(input_path):
    if input_path.endswith(".wav"):                       # convert any audio format to wav for whisper api
        return input_path
    try:
        from pydub import AudioSegment
        ext = os.path.splitext(input_path)[-1].lower().lstrip(".")
        audio = AudioSegment.from_file(input_path, format=ext if ext else "mp3")
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio.export(tmp.name, format="wav")
        return tmp.name
    except Exception as e:
        raise RuntimeError(f"audio conversion failed: {e}")