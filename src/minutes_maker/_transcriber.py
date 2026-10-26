import os
from functools import lru_cache

SUPPORTED_LANGS = {"en", "te", "hi"}

MODEL_NAME = os.environ.get("WHISPER_MODEL", "tiny")
DEVICE = "cuda" if os.environ.get("USE_CUDA", "0") == "1" else "cpu"
COMPUTE_TYPE = os.environ.get("WHISPER_COMPUTE_TYPE", "int8")


@lru_cache(maxsize=1)
def load_model():
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "faster-whisper is not installed. Install requirements.txt to enable transcription."
        ) from exc

    return WhisperModel(MODEL_NAME, device=DEVICE, compute_type=COMPUTE_TYPE)


def transcribe_segment(audio_path: str, language: str = "en") -> str:
    if language not in SUPPORTED_LANGS:
        raise ValueError("Only English, Telugu, and Hindi are supported.")

    model = load_model()
    segments, _info = model.transcribe(audio_path, language=language, vad_filter=True)
    return " ".join(s.text.strip() for s in segments if s.text and s.text.strip())
