import { Box, Typography } from "@mui/material";

const Title: React.FC = () => {
  return (
    <Box className="title-block">
      <Typography variant="h3" component="h1" fontWeight={800}>
        AI-Based Smart Meeting Minutes Generator
      </Typography>
      <Typography color="text.secondary">
        Upload a recording to create speaker-labeled summaries, decisions, action items, keywords,
        and professional PDF/DOCX reports.
      </Typography>
    </Box>
  );
};

export { Title };
