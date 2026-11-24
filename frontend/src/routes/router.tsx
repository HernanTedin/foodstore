import { Navigate, createBrowserRouter } from "react-router";

import LoginPage from "@/features/auth/pages/LoginPage";
import PanelPage from "@/pages/PanelPage";
import { useAuthStore } from "@/store/authStore";
import RegisterPage from "@/features/auth/pages/RegisterPage";
/** Ruta protegida: sin sesión, redirige al login. */
// eslint-disable-next-line react-refresh/only-export-components
function Protegida({ children }: { children: React.ReactNode }) {
  const status = useAuthStore((s) => s.status);
  if (status === "checking")
    return <p className="p-8 text-navy-500">Cargando…</p>;
  if (status === "anonymous") return <Navigate to="/login" replace />;
  return children;
}

export const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  { path: "/register", element: <RegisterPage /> },
  {
    path: "/",
    element: (
      <Protegida>
        <PanelPage />
      </Protegida>
    ),
  },
]);
