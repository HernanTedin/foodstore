import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

/**
 * Cliente HTTP único.
 * - withCredentials: el navegador adjunta la cookie HttpOnly. El token nunca
 *   es accesible desde JavaScript.
 * - Ante un 401 reintenta UNA vez llamando a /auth/refresh.
 */
export const api = axios.create({
  baseURL: "/api/v1",
  withCredentials: true,
  headers: { Accept: "application/json" },
});

type RetriableConfig = InternalAxiosRequestConfig & { _retry?: boolean };

const SIN_REFRESH = ["/auth/token", "/auth/refresh", "/auth/register"];

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as RetriableConfig | undefined;
    const url = original?.url ?? "";
    const esRutaDeAuth = SIN_REFRESH.some((ruta) => url.endsWith(ruta));

    if (
      error.response?.status !== 401 ||
      !original ||
      original._retry ||
      esRutaDeAuth
    ) {
      return Promise.reject(error);
    }

    original._retry = true;
    await api.post("/auth/refresh");
    return api(original);
  },
);
