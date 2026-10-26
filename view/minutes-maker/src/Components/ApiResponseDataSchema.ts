type TranscriptSegment = {
  speaker: string;
  start: number;
  end: number;
  text: string;
};

type ApiResponseDataSchema = {
  title: string;
  summary: string;
  decisions: string[];
  action_items: string[];
  keywords: string[];
  diarized_transcript: TranscriptSegment[];
  pdf: string;
  docx: string;
};

export type { ApiResponseDataSchema, TranscriptSegment };
