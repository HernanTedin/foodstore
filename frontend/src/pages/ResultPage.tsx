import { Link, useLocation } from "react-router";

import { cn } from "@/shared/lib/cn";

/**
 * Feedback por rutas: el resultado de una acción navega a /success o /error
 * y manda el texto en location.state. Sin avisos flotantes.
 */
export interface ResultState {
  title?: string;
  message?: string;
  to?: string;
  cta?: string;
}

const DEFAULTS = {
  success: {
    title: "Listo",
    message: "La operación se completó correctamente.",
  },
  error: {
    title: "Algo salió mal",
    message: "No pudimos completar la operación.",
  },
} as const;

export function ResultPage({ kind }: { kind: "success" | "error" }) {
  const state = (useLocation().state ?? {}) as ResultState;
  const exito = kind === "success";

  return (
    <div className="mx-auto flex max-w-md flex-col px-4 py-16">
      <div className="flex flex-col items-center gap-4 rounded-xl border border-surface-border bg-surface p-8 text-center">
        <span
          aria-hidden="true"
          className={cn(
            "grid size-14 place-items-center rounded-full text-2xl font-bold text-white",
            exito ? "bg-success-600" : "bg-danger-600",
          )}
        >
          {exito ? "✓" : "!"}
        </span>
        <h1 className="text-xl font-bold text-navy-900">
          {state.title ?? DEFAULTS[kind].title}
        </h1>
        <p className="text-sm text-navy-700">
          {state.message ?? DEFAULTS[kind].message}
        </p>
        <Link
          to={state.to ?? "/"}
          className="mt-2 inline-flex h-10 items-center rounded-lg bg-accent-600 px-5 text-sm font-semibold text-white hover:bg-accent-700"
        >
          {state.cta ?? "Volver"}
        </Link>
      </div>
    </div>
  );
}

export function SuccessPage() {
  return <ResultPage kind="success" />;
}

export function ErrorPage() {
  return <ResultPage kind="error" />;
}
