import { useState } from "react";
import "./App.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import { FileUploader } from "./Components/FileUploader";
import { ResultDisplay } from "./Components/ResultDisplay";
import { AppContext } from "./Components/AppContext";
import { ApiResponseDataSchema } from "./Components/ApiResponseDataSchema";
import { Title } from "./Components/Title";

function App() {
  const [apiResponse, setApiResponse] = useState<ApiResponseDataSchema | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const theme = createTheme({
    palette: {
      primary: {
        main: "#345995",
      },
      secondary: {
        main: "#2f9c95",
      },
      background: {
        default: "#f4f6f8",
      },
    },
    shape: {
      borderRadius: 8,
    },
    typography: {
      fontFamily: "Inter, Ubuntu, Arial, sans-serif",
    },
  });

  return (
    <AppContext.Provider value={{ apiResponse, isLoading }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <main className="App">
          <Title />
          <FileUploader setApiResponse={setApiResponse} setIsLoading={setIsLoading} />
          <ResultDisplay />
        </main>
      </ThemeProvider>
    </AppContext.Provider>
  );
}

export default App;
