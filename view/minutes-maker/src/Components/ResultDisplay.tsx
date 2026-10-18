import React, { useContext } from "react";
import { AppContext } from "./AppContext";
import ReactMarkdown from "react-markdown";
import {
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import { API_BASE_URL } from "./FileUploader";

const renderList = (items: string[], emptyText: string) =>
  items.length ? (
    <ul className="result-list">
      {items.map((item, index) => (
        <li key={`${item}-${index}`}>{item}</li>
      ))}
    </ul>
  ) : (
    <Typography color="text.secondary">{emptyText}</Typography>
  );

const ResultDisplay: React.FC = () => {
  const { apiResponse, isLoading } = useContext(AppContext);

  if (isLoading) {
    return (
      <Box className="loading-state">
        <CircularProgress />
        <Typography color="text.secondary">Generating transcript, summary, actions, and reports...</Typography>
      </Box>
    );
  }

  if (!apiResponse) {
    return null;
  }

  return (
    <Box className="results-grid">
      <Paper className="result-card summary-card">
        <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" spacing={2}>
          <Box>
            <Typography variant="h5" fontWeight={700}>
              {apiResponse.title}
            </Typography>
            <Typography color="text.secondary">Smart meeting report</Typography>
          </Box>
          <Stack direction="row" spacing={1}>
            <Button variant="outlined" href={`${API_BASE_URL}${apiResponse.pdf}`} target="_blank">
              PDF
            </Button>
            <Button variant="outlined" href={`${API_BASE_URL}${apiResponse.docx}`} target="_blank">
              DOCX
            </Button>
          </Stack>
        </Stack>
        <Divider sx={{ my: 2 }} />
        <Typography variant="h6">Summary</Typography>
        <ReactMarkdown>{apiResponse.summary}</ReactMarkdown>
      </Paper>

      <Paper className="result-card">
        <Typography variant="h6">Action Items</Typography>
        {renderList(apiResponse.action_items, "No action items detected.")}
      </Paper>

      <Paper className="result-card">
        <Typography variant="h6">Decisions</Typography>
        {renderList(apiResponse.decisions, "No decisions detected.")}
      </Paper>

      <Paper className="result-card">
        <Typography variant="h6">Keywords</Typography>
        <Stack direction="row" gap={1} flexWrap="wrap" mt={2}>
          {apiResponse.keywords.length ? (
            apiResponse.keywords.map((keyword) => <Chip key={keyword} label={keyword} />)
          ) : (
            <Typography color="text.secondary">No keywords detected.</Typography>
          )}
        </Stack>
      </Paper>

      <Paper className="result-card transcript-card">
        <Typography variant="h6">Diarized Transcript</Typography>
        <Stack spacing={2} mt={2}>
          {apiResponse.diarized_transcript.map((segment, index) => (
            <Box key={`${segment.speaker}-${segment.start}-${index}`} className="transcript-line">
              <Typography fontWeight={700}>
                {segment.speaker} [{segment.start.toFixed(1)}-{segment.end.toFixed(1)}]
              </Typography>
              <Typography color={segment.text ? "text.primary" : "text.secondary"}>
                {segment.text || "No speech transcribed for this segment."}
              </Typography>
            </Box>
          ))}
        </Stack>
      </Paper>
    </Box>
  );
};

export { ResultDisplay };
