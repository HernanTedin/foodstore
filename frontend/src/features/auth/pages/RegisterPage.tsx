import { useMutation } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";

import { authApi } from "@/features/auth/api/authApi";
import { requisitosPendientes } from "@/features/auth/types/auth";
import { toApiError } from "@/shared/api/apiError";

const INPUT =
  "mt-1 w-full rounded-lg border border-surface-border px-3 py-2 text-navy-900 outline-none focus:border-accent-600";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    nombre: "",
    apellido: "",
    email: "",
    telefono: "",
    password: "",
  });

  const registro = useMutation({
    mutationFn: authApi.register,
    // Tras registrarse, se manda al login para que ingrese con su cuenta nueva.
    onSuccess: () => navigate("/login", { replace: true }),
  });

  const error = registro.error ? toApiError(registro.error) : null;
  const faltan = form.password ? requisitosPendientes(form.password) : [];

  function cambiar(campo: keyof typeof form, valor: string) {
    setForm((f) => ({ ...f, [campo]: valor }));
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (faltan.length > 0) return;
    registro.mutate({ ...form, telefono: form.telefono || undefined });
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-surface-muted p-4">
      <form
        onSubmit={onSubmit}
        className="w-full max-w-sm space-y-4 rounded-xl border border-surface-border bg-surface p-6 shadow-sm"
      >
        <h1 className="text-2xl font-bold text-navy-900">Crear cuenta</h1>

        <div className="grid grid-cols-2 gap-3">
          <label className="block text-sm font-medium text-navy-700">
            Nombre
            <input
              required
              className={INPUT}
              value={form.nombre}
              onChange={(e) => cambiar("nombre", e.target.value)}
            />
          </label>
          <label className="block text-sm font-medium text-navy-700">
            Apellido
            <input
              required
              className={INPUT}
              value={form.apellido}
              onChange={(e) => cambiar("apellido", e.target.value)}
            />
          </label>
        </div>

        <label className="block text-sm font-medium text-navy-700">
          Email
          <input
            type="email"
            required
            className={INPUT}
            value={form.email}
            onChange={(e) => cambiar("email", e.target.value)}
          />
        </label>

        <label className="block text-sm font-medium text-navy-700">
          Teléfono (opcional)
          <input
            type="tel"
            className={INPUT}
            value={form.telefono}
            onChange={(e) => cambiar("telefono", e.target.value)}
          />
        </label>

        <label className="block text-sm font-medium text-navy-700">
          Contraseña
          <input
            type="password"
            required
            className={INPUT}
            value={form.password}
            onChange={(e) => cambiar("password", e.target.value)}
          />
        </label>
        {faltan.length > 0 && (
          <p className="text-sm text-navy-500">Falta: {faltan.join(", ")}.</p>
        )}

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
          disabled={registro.isPending || faltan.length > 0}
          className="w-full rounded-lg bg-accent-600 px-4 py-2 font-medium text-white hover:bg-accent-700 disabled:opacity-60"
        >
          {registro.isPending ? "Creando…" : "Crear cuenta"}
        </button>

        <p className="text-center text-sm text-navy-500">
          ¿Ya tenés cuenta?{" "}
          <Link
            to="/login"
            className="font-medium text-accent-700 hover:underline"
          >
            Ingresar
          </Link>
        </p>
      </form>
    </main>
  );
}
