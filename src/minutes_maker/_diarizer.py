import os
from functools import lru_cache


@lru_cache(maxsize=1)
def load_pipeline():
    try:
        from pyannote.audio import Pipeline
    except ImportError as exc:
        raise RuntimeError(
            "pyannote.audio is not installed. Install requirements.txt to enable speaker diarization."
        ) from exc

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    try:
        return Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", token=token)
    except TypeError:
        return Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)


def diarize(audio_path: str) -> list[dict]:
    """
    Return diarized segments as {speaker, start, end}. Requires a Hugging Face token
    for pyannote's gated model; callers should provide a fallback when unavailable.
    """
    diarization = load_pipeline()(audio_path)
    segments = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append(
            {
                "speaker": str(speaker).replace("SPEAKER_", "Speaker "),
                "start": round(float(turn.start), 2),
                "end": round(float(turn.end), 2),
            }
        )

    return segments
