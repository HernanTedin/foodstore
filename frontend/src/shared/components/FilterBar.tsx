import { useEffect, useState, type ReactNode } from "react";

export type EstadoFiltro = "activos" | "inactivos" | "todos";

interface FilterBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  estado: EstadoFiltro;
  onEstadoChange: (value: EstadoFiltro) => void;
  /** Combo extra de agrupación (por ejemplo, rol). */
  extra?: ReactNode;
  placeholder?: string;
  debounceMs?: number;
}

const ESTADOS: { value: EstadoFiltro; label: string }[] = [
  { value: "activos", label: "Activos" },
  { value: "inactivos", label: "Inactivos" },
  { value: "todos", label: "Todos" },
];

/** Buscador (espera unos 400 ms antes de buscar) + filtro Activos / Inactivos / Todos. */
export function FilterBar({
  search,
  onSearchChange,
  estado,
  onEstadoChange,
  extra,
  placeholder = "Buscar…",
  debounceMs = 400,
}: FilterBarProps) {
  const [texto, setTexto] = useState(search);

  useEffect(() => {
    const id = window.setTimeout(() => {
      if (texto !== search) onSearchChange(texto);
    }, debounceMs);
    return () => window.clearTimeout(id);
  }, [texto, search, onSearchChange, debounceMs]);

  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      <input
        type="search"
        aria-label="Buscar"
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder={placeholder}
        className="h-10 flex-1 rounded-lg border border-surface-border bg-surface px-3 text-sm focus-visible:ring-2 focus-visible:ring-accent-600 focus-visible:outline-none"
      />
      {extra}
      <div
        role="group"
        aria-label="Estado"
        className="inline-flex rounded-lg border border-surface-border bg-surface p-0.5"
      >
        {ESTADOS.map((op) => (
          <button
            key={op.value}
            type="button"
            aria-pressed={estado === op.value}
            onClick={() => onEstadoChange(op.value)}
            className="rounded-md px-3 py-1.5 text-sm text-navy-700 focus-visible:ring-2 focus-visible:ring-accent-600 focus-visible:outline-none aria-pressed:bg-navy-900 aria-pressed:text-white"
          >
            {op.label}
          </button>
        ))}
      </div>
    </div>
  );
}
