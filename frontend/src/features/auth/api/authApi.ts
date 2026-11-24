import { api } from "@/shared/api/axiosInstance";
import type { Usuario } from "@/shared/types/api";

export interface LoginInput {
  email: string;
  password: string;
}
export interface RegisterInput {
  nombre: string;
  apellido: string;
  email: string;
  telefono?: string;
  password: string;
}
/** Llamadas HTTP del módulo auth. Los tokens nunca pasan por acá: viajan en cookies. */
export const authApi = {
  async me(): Promise<Usuario> {
    const { data } = await api.get<Usuario>("/auth/me");
    return data;
  },

  async login({ email, password }: LoginInput): Promise<Usuario> {
    // OAuth2 Password Flow: x-www-form-urlencoded con username y password.
    const body = new URLSearchParams({ username: email, password });
    const { data } = await api.post<Usuario>("/auth/token", body);
    return data;
  },

  async logout(): Promise<void> {
    await api.post("/auth/logout");
  },
  async register(input: RegisterInput): Promise<Usuario> {
    const { data } = await api.post<Usuario>("/auth/register", input);
    return data;
  },
};
