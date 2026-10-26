import os
import re
import tempfile
from pathlib import Path

from pydub import AudioSegment


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem or "meeting"
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", stem).strip("._") or "meeting"


def get_audio_duration(source_path: str) -> float:
    audio = AudioSegment.from_file(source_path)
    return round(len(audio) / 1000, 2)


def extract_audio_chunk(source_path: str, start: float, end: float) -> str:
    audio = AudioSegment.from_file(source_path)
    start_ms = max(0, int(start * 1000))
    end_ms = min(len(audio), int(end * 1000))

    fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)

    audio[start_ms:end_ms].export(out_path, format="wav")
    return out_path
