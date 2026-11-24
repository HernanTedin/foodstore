import { useMutation } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { useNavigate, Link } from "react-router";

import { authApi } from "@/features/auth/api/authApi";
import { toApiError } from "@/shared/api/apiError";
import { useAuthStore } from "@/store/authStore";

export default function LoginPage() {
  const navigate = useNavigate();
  const setUsuario = useAuthStore((s) => s.setUsuario);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = useMutation({
    mutationFn: authApi.login,
    onSuccess: (usuario) => {
      setUsuario(usuario);
      navigate("/", { replace: true });
    },
  });

  const error = login.error ? toApiError(login.error) : null;

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    login.mutate({ email, password });
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-surface-muted p-4">
      <form
        onSubmit={onSubmit}
        className="w-full max-w-sm space-y-4 rounded-xl border border-surface-border bg-surface p-6 shadow-sm"
      >
        <h1 className="text-2xl font-bold text-navy-900">
          Ingresar a Food Store
        </h1>

        <label className="block text-sm font-medium text-navy-700">
          Email
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full rounded-lg border border-surface-border px-3 py-2 text-navy-900 outline-none focus:border-accent-600"
          />
        </label>

        <label className="block text-sm font-medium text-navy-700">
          Contraseña
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded-lg border border-surface-border px-3 py-2 text-navy-900 outline-none focus:border-accent-600"
          />
        </label>

        {error && (
          <p
            role="alert"
            className="rounded-lg bg-danger-50 px-3 py-2 text-sm text-danger-600"
          >
            {error.detail}
          </p>
        )}

        <button
          type="submit"
          disabled={login.isPending}
          className="w-full rounded-lg bg-accent-600 px-4 py-2 font-medium text-white hover:bg-accent-700 disabled:opacity-60"
        >
          {login.isPending ? "Ingresando…" : "Ingresar"}
        </button>
        <p className="text-center text-sm text-navy-500">
          ¿No tenés cuenta?{" "}
          <Link
            to="/register"
            className="font-medium text-accent-700 hover:underline"
          >
            Crear cuenta
          </Link>
        </p>
      </form>
    </main>
  );
}
