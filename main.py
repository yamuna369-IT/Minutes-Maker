import argparse
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from minutes_maker import process_meeting
from minutes_maker.utils import safe_stem

REPORT_DIR = Path("generated_reports")


class TranscriptSegment(BaseModel):
    speaker: str
    start: float
    end: float
    text: str


class OutputData(BaseModel):
    title: str
    summary: str
    decisions: list[str]
    action_items: list[str]
    keywords: list[str]
    diarized_transcript: list[TranscriptSegment]
    pdf: str
    docx: str


class MinutesMakerAPI:
    def __init__(self):
        self.app = FastAPI(title="AI-Based Smart Meeting Minutes Generator")
        REPORT_DIR.mkdir(exist_ok=True)

        self.app.add_api_route(
            "/minutes_maker",
            self.minutes_maker,
            methods=["POST"],
            response_model=OutputData,
        )
        self.app.add_api_route("/reports/{filename}", self.download_report, methods=["GET"])

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def minutes_maker(
        self,
        file: UploadFile = File(...),
        filename: str = Form(...),
        language: str = Form("en"),
        category: str = Form("meeting"),
        content: str = Form("Meeting Minutes"),
    ) -> OutputData:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        title = f"{content.strip() or 'Meeting Minutes'} ({category})"

        with TemporaryDirectory() as tempdir:
            safe_name = safe_stem(filename) + Path(filename).suffix
            audio_path = Path(tempdir) / safe_name
            audio_path.write_bytes(file_bytes)

            result = process_meeting(
                str(audio_path),
                language=language,
                title=title,
                output_dir=REPORT_DIR,
            )

        pdf_name = Path(result["pdf_path"]).name
        docx_name = Path(result["docx_path"]).name
        report = result["report"]

        return OutputData(
            title=report["title"],
            summary=report["summary"],
            decisions=report["decisions"],
            action_items=report["action_items"],
            keywords=report["keywords"],
            diarized_transcript=report["diarized_transcript"],
            pdf=f"/reports/{pdf_name}",
            docx=f"/reports/{docx_name}",
        )

    async def download_report(self, filename: str):
        requested = REPORT_DIR / Path(filename).name
        if not requested.exists():
            raise HTTPException(status_code=404, detail="Report not found.")
        return FileResponse(str(requested), filename=requested.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=10355)
    args = parser.parse_args()

    api = MinutesMakerAPI()
    uvicorn.run(api.app, host="0.0.0.0", port=args.port)
