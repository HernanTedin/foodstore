import { isAxiosError } from "axios";

import type { ApiError } from "@/shared/types/api";

const ERROR_GENERICO: ApiError = {
  detail:
    "No pudimos conectar con el servidor. Probá de nuevo en unos segundos.",
  code: "NETWORK_ERROR",
  field: null,
};

function esApiError(data: unknown): data is ApiError {
  return (
    typeof data === "object" &&
    data !== null &&
    "detail" in data &&
    "code" in data
  );
}

/** Convierte cualquier error de axios al formato estándar de la API. */
export function toApiError(error: unknown): ApiError {
  if (isAxiosError(error) && esApiError(error.response?.data)) {
    return error.response.data;
  }
  return ERROR_GENERICO;
}
