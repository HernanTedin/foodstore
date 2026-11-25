import { isAxiosError } from "axios";

/** Saca el mensaje de error que mandó el backend ({detail, code, field}). */
export function mensajeError(error: unknown): string {
  if (isAxiosError(error) && typeof error.response?.data?.detail === "string") {
    return error.response.data.detail;
  }
  return "No pudimos completar la operación. Intenta nuevamente.";
}
