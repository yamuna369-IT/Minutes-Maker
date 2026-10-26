import { createContext } from "react";
import { ApiResponseDataSchema } from "./ApiResponseDataSchema";

interface AppContextProps {
  apiResponse: ApiResponseDataSchema | null;
  isLoading: boolean;
}

const AppContext = createContext<AppContextProps>({
  apiResponse: null,
  isLoading: false,
});

export { AppContext };
