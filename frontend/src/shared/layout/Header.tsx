import { useNavigate } from "react-router";

import { authApi } from "@/features/auth/api/authApi";
import { ROL_NOMBRE } from "@/shared/layout/navigation";
import { useAuthStore } from "@/store/authStore";

export function Header() {
  const navigate = useNavigate();
  const usuario = useAuthStore((s) => s.usuario);
  const clearSession = useAuthStore((s) => s.clearSession);

  if (!usuario) return null;
  const iniciales =
    `${usuario.nombre[0] ?? ""}${usuario.apellido[0] ?? ""}`.toUpperCase();

  async function salir() {
    await authApi.logout();
    clearSession();
    navigate("/login", { replace: true });
  }

  return (
    <header className="flex items-center justify-between border-b border-surface-border bg-surface px-6 py-3">
      <p className="font-semibold text-navy-900 md:hidden">
        Food <span className="text-accent-600">Store</span>
      </p>
      <div className="ml-auto flex items-center gap-4">
        <div className="text-right">
          <p className="text-sm font-medium text-navy-900">
            {usuario.nombre} {usuario.apellido}
          </p>
          <p className="text-xs text-navy-500">
            {usuario.roles.map((r) => ROL_NOMBRE[r]).join(" · ")}
          </p>
        </div>
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-accent-100 text-sm font-semibold text-accent-700">
          {iniciales}
        </span>
        <button
          onClick={salir}
          className="rounded-lg border border-surface-border px-3 py-1.5 text-sm text-navy-700 hover:bg-surface-muted"
        >
          Cerrar sesión
        </button>
      </div>
    </header>
  );
}
