interface PaginacionProps {
  page: number;
  pages: number;
  total: number;
  onChange: (page: number) => void;
}

const BOTON =
  "h-8 rounded-lg border border-surface-border bg-surface px-3 text-sm text-navy-900 hover:bg-surface-muted disabled:cursor-not-allowed disabled:opacity-60";

export function Paginacion({ page, pages, total, onChange }: PaginacionProps) {
  if (pages <= 1) return null;
  return (
    <nav
      aria-label="Paginación"
      className="flex items-center justify-between gap-4 border-t border-surface-border px-4 py-3 text-sm"
    >
      <p className="text-navy-500">
        Página {page} de {pages} · {total} registros
      </p>
      <div className="flex gap-2">
        <button
          type="button"
          className={BOTON}
          disabled={page <= 1}
          onClick={() => onChange(page - 1)}
        >
          Anterior
        </button>
        <button
          type="button"
          className={BOTON}
          disabled={page >= pages}
          onClick={() => onChange(page + 1)}
        >
          Siguiente
        </button>
      </div>
    </nav>
  );
}
