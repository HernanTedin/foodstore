import { create } from "zustand";

import type { RolCodigo, Usuario } from "@/shared/types/api";

/**
 * Sesión del usuario (estado del cliente). No persiste: al recargar,
 * GET /auth/me reconstruye la sesión. El token vive en la cookie HttpOnly.
 */
export type SessionStatus = "checking" | "authenticated" | "anonymous";

interface AuthState {
  usuario: Usuario | null;
  status: SessionStatus;
  setUsuario: (usuario: Usuario) => void;
  clearSession: () => void;
  hasRole: (...roles: RolCodigo[]) => boolean;
}

export const useAuthStore = create<AuthState>()((set, get) => ({
  usuario: null,
  status: "checking",
  setUsuario: (usuario) => set({ usuario, status: "authenticated" }),
  clearSession: () => set({ usuario: null, status: "anonymous" }),
  hasRole: (...roles) => {
    const propios = get().usuario?.roles ?? [];
    return roles.some((rol) => propios.includes(rol));
  },
}));
