import json
import os
import re
from collections import Counter

LANG_MAP = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
}

PROMPT = """
You are an AI meeting minutes assistant.

Create professional meeting minutes from the diarized transcript.
Return only valid JSON using this schema:
{
  "summary": "5-8 concise sentences in the transcript language",
  "decisions": ["decision 1"],
  "action_items": ["Task - Assignee - Deadline"],
  "keywords": ["keyword"]
}

Rules:
- Preserve concrete names, dates, owners, decisions, and follow-ups.
- If an assignee or deadline is missing, write "Unassigned" or "No deadline".
- Use {lang_name}.

TRANSCRIPT:
{transcript}
"""


def format_transcript(segments: list[dict]) -> str:
    lines = []
    for segment in segments:
        text = segment.get("text", "").strip()
        if text:
            lines.append(
                f"{segment['speaker']} [{segment['start']:.1f}-{segment['end']:.1f}]: {text}"
            )
    return "\n".join(lines)


def _parse_json(content: str) -> dict:
    content = content.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
    if fenced:
        content = fenced.group(1).strip()
    return json.loads(content)


def _fallback_minutes(segments: list[dict]) -> dict:
    transcript = " ".join(s.get("text", "").strip() for s in segments if s.get("text"))
    sentences = re.split(r"(?<=[.!?])\s+", transcript)
    sentences = [s.strip() for s in sentences if s.strip()]
    summary = " ".join(sentences[:6]) if sentences else "No transcribed speech was available."

    words = re.findall(r"[A-Za-z][A-Za-z0-9-]{3,}", transcript.lower())
    stop_words = {
        "about",
        "after",
        "also",
        "from",
        "have",
        "meeting",
        "that",
        "this",
        "with",
        "will",
        "would",
        "your",
    }
    keywords = [word for word, _count in Counter(w for w in words if w not in stop_words).most_common(10)]

    action_sentences = [
        sentence
        for sentence in sentences
        if re.search(r"\b(action|assign|follow up|deadline|todo|task|owner|next)\b", sentence, re.I)
    ]
    decision_sentences = [
        sentence
        for sentence in sentences
        if re.search(r"\b(decided|decision|approved|agreed|confirmed|finalized)\b", sentence, re.I)
    ]

    return {
        "summary": summary,
        "decisions": decision_sentences[:8],
        "action_items": action_sentences[:8],
        "keywords": keywords,
    }


def _normalize_minutes(data: dict, segments: list[dict]) -> dict:
    fallback = _fallback_minutes(segments)
    return {
        "summary": str(data.get("summary") or fallback["summary"]),
        "decisions": list(data.get("decisions") or fallback["decisions"]),
        "action_items": list(data.get("action_items") or fallback["action_items"]),
        "keywords": list(data.get("keywords") or fallback["keywords"]),
    }


def extract_meeting_info(segments: list[dict], language: str) -> dict:
    llm_input = format_transcript(segments)
    if not llm_input:
        return _fallback_minutes(segments)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return _fallback_minutes(segments)

    prompt = PROMPT.format(transcript=llm_input, lang_name=LANG_MAP.get(language, "English"))
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    try:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
        except ImportError:
            import openai

            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            content = response.choices[0].message["content"]

        return _normalize_minutes(_parse_json(content), segments)
    except Exception:
        return _fallback_minutes(segments)
