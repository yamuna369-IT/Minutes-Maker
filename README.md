# AI-Based Smart Meeting Minutes Generator

This project generates professional meeting minutes from audio or video recordings. It combines Faster-Whisper transcription, optional pyannote speaker diarization, OpenAI-compatible LLM summarization, and PDF/DOCX report export.

## Features

- Audio/video upload from the React web interface
- Faster-Whisper speech-to-text transcription
- Optional speaker diarization with pyannote and `HF_TOKEN`
- English, Telugu, and Hindi input support
- LLM-generated summaries, decisions, action items, and keywords
- Local fallback summarization when `OPENAI_API_KEY` is not set
- PDF and DOCX meeting report generation
- Download links for generated reports

## Setup

Install backend dependencies:

```bash
python -m pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd view/minutes-maker
npm install
```

Create a `.env` file or set environment variables:

```bash
OPENAI_API_KEY=sk-your-key
HF_TOKEN=hf-your-token
REACT_APP_PUBLIC_IP=localhost
WHISPER_MODEL=tiny
```

`OPENAI_API_KEY` is optional, but recommended for high-quality summaries. `HF_TOKEN` is optional; without it the app still transcribes the full recording as `Speaker 1`.
Use `WHISPER_MODEL=tiny` for quick local demos, or `small`/`medium` for better accuracy.

## Run

Backend:

```bash
python main.py --port 10355
```

Frontend:

```bash
cd view/minutes-maker
npm start
```

Open `http://localhost:3000`.

## Production Build

```bash
cd view/minutes-maker
npm run build
```

Generated reports are stored in `generated_reports/` and served from `/reports/<filename>`.
