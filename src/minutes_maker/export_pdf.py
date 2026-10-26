from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _section(story: list, styles, title: str, body) -> None:
    story.append(Paragraph(title, styles["Heading2"]))
    if isinstance(body, list):
        values = body or ["No items detected."]
        for item in values:
            story.append(Paragraph(f"- {item}", styles["BodyText"]))
    else:
        story.append(Paragraph(str(body or "No content detected."), styles["BodyText"]))
    story.append(Spacer(1, 12))


def export_pdf(data: dict, out_path: str) -> str:
    doc = SimpleDocTemplate(out_path, pagesize=A4, rightMargin=40, leftMargin=40)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(data["title"], styles["Title"]),
        Paragraph(f"Generated: {data['date']} | Language: {data['language'].upper()}", styles["BodyText"]),
        Spacer(1, 16),
    ]

    _section(story, styles, "Executive Summary", data["summary"])
    _section(story, styles, "Key Decisions", data["decisions"])
    _section(story, styles, "Action Items", data["action_items"])
    _section(story, styles, "Keywords", ", ".join(data["keywords"]))

    story.append(Paragraph("Diarized Transcript", styles["Heading2"]))
    for segment in data["diarized_transcript"]:
        text = segment.get("text", "").strip()
        if not text:
            continue
        story.append(
            Paragraph(
                f"<b>{segment['speaker']} [{segment['start']:.1f}-{segment['end']:.1f}]</b>: {text}",
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 6))

    doc.build(story)
    return out_path
