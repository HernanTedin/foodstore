import { useEffect } from "react";
import { RouterProvider } from "react-router";

import { authApi } from "@/features/auth/api/authApi";
import { router } from "@/routes/router";
import { useAuthStore } from "@/store/authStore";
import { ConfirmModal } from "@/shared/ui/ConfirmModal";
export default function App() {
  const setUsuario = useAuthStore((s) => s.setUsuario);
  const clearSession = useAuthStore((s) => s.clearSession);

  // Al cargar la app se consulta /auth/me para reconstruir la sesión desde la cookie.
  useEffect(() => {
    authApi.me().then(setUsuario).catch(clearSession);
  }, [setUsuario, clearSession]);

  return (
    <>
      <RouterProvider router={router} />
      <ConfirmModal />
    </>
  );
}
