import os
import time
from pathlib import Path

from ._diarizer import diarize
from ._summarizer import extract_meeting_info
from ._transcriber import transcribe_segment
from .export_docx import export_docx
from .export_pdf import export_pdf
from .utils import extract_audio_chunk, get_audio_duration, safe_stem

SUPPORTED_LANGS = {"en", "te", "hi"}


def _fallback_segments(audio_path: str) -> list[dict]:
    return [{"speaker": "Speaker 1", "start": 0.0, "end": get_audio_duration(audio_path)}]


def _merge_short_segments(segments: list[dict], min_seconds: float = 1.0) -> list[dict]:
    clean_segments = [s for s in segments if s["end"] - s["start"] >= min_seconds]
    return clean_segments or segments


def process_meeting(
    audio_path: str,
    language: str = "en",
    title: str = "Meeting Minutes",
    output_dir: str | os.PathLike | None = None,
) -> dict:
    if language not in SUPPORTED_LANGS:
        raise ValueError("Only English, Telugu, and Hindi are supported.")

    try:
        diarized_segments = _merge_short_segments(diarize(audio_path))
    except Exception:
        diarized_segments = _fallback_segments(audio_path)

    final_segments = []
    temp_files = []
    for segment in diarized_segments:
        chunk_path = extract_audio_chunk(audio_path, segment["start"], segment["end"])
        temp_files.append(chunk_path)
        try:
            text = transcribe_segment(chunk_path, language)
        except Exception:
            text = ""

        final_segments.append(
            {
                "speaker": segment["speaker"],
                "start": segment["start"],
                "end": segment["end"],
                "text": text,
            }
        )

    minutes = extract_meeting_info(final_segments, language)
    report_data = {
        "title": title or "Meeting Minutes",
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "language": language,
        "summary": minutes["summary"],
        "decisions": minutes["decisions"],
        "action_items": minutes["action_items"],
        "keywords": minutes["keywords"],
        "diarized_transcript": final_segments,
    }

    output_path = Path(output_dir or Path(audio_path).parent)
    output_path.mkdir(parents=True, exist_ok=True)
    base_name = f"{safe_stem(audio_path)}_{int(time.time())}"
    docx_path = output_path / f"{base_name}_report.docx"
    pdf_path = output_path / f"{base_name}_report.pdf"

    export_docx(report_data, str(docx_path))
    export_pdf(report_data, str(pdf_path))

    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except OSError:
            pass

    return {
        "report": report_data,
        "docx_path": str(docx_path),
        "pdf_path": str(pdf_path),
    }
