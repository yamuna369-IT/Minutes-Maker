import React, { useState } from "react";
import axios from "axios";
import { ApiResponseDataSchema } from "./ApiResponseDataSchema";
import {
  Alert,
  Box,
  Button,
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Stack,
  TextField,
} from "@mui/material";

interface FileUploaderProps {
  setApiResponse: React.Dispatch<React.SetStateAction<ApiResponseDataSchema | null>>;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const API_HOST = process.env.REACT_APP_PUBLIC_IP || "localhost";
const API_BASE_URL = `http://${API_HOST}:10355`;

const FileUploader: React.FC<FileUploaderProps> = ({ setApiResponse, setIsLoading }) => {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState<string>("en");
  const [category, setCategory] = useState<string>("meeting");
  const [content, setContent] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");

    if (!file || !content.trim()) {
      setError("Upload a recording and enter a meeting topic.");
      return;
    }

    setIsLoading(true);
    setApiResponse(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("filename", file.name);
    formData.append("language", language);
    formData.append("category", category);
    formData.append("content", content.trim());

    try {
      const response = await axios.post<ApiResponseDataSchema>(
        `${API_BASE_URL}/minutes_maker`,
        formData
      );
      setApiResponse(response.data);
    } catch (requestError) {
      setError("Unable to generate minutes. Check that the backend is running and the recording is valid.");
      console.error(requestError);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} className="upload-panel" noValidate>
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}

        <TextField
          variant="outlined"
          required
          fullWidth
          name="file"
          type="file"
          inputProps={{ accept: "audio/*,video/*" }}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
            setFile(event.target.files ? event.target.files[0] : null)
          }
          helperText="Upload an audio or video meeting recording."
        />

        <FormControl>
          <FormLabel>Language</FormLabel>
          <RadioGroup
            row
            aria-label="language"
            name="language"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
          >
            <FormControlLabel value="en" control={<Radio />} label="English" />
            <FormControlLabel value="te" control={<Radio />} label="Telugu" />
            <FormControlLabel value="hi" control={<Radio />} label="Hindi" />
          </RadioGroup>
        </FormControl>

        <FormControl>
          <FormLabel>Category</FormLabel>
          <RadioGroup
            row
            aria-label="category"
            name="category"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
          >
            <FormControlLabel value="meeting" control={<Radio />} label="Meeting" />
            <FormControlLabel value="lecture" control={<Radio />} label="Lecture" />
          </RadioGroup>
        </FormControl>

        <TextField
          required
          fullWidth
          label="Meeting topic"
          value={content}
          onChange={(event) => setContent(event.target.value)}
          placeholder="e.g. Product planning sync"
        />

        <Button variant="contained" size="large" type="submit">
          Generate Minutes
        </Button>
      </Stack>
    </Box>
  );
};

export { FileUploader, API_BASE_URL };
