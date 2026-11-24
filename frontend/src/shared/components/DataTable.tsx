import type { ReactNode } from "react";

import { EstadoVacio } from "@/shared/components/EstadoVacio";
import { SkeletonRows } from "@/shared/components/Skeleton";
import { cn } from "@/shared/lib/cn";

export interface Column<T> {
  key: string;
  header: string;
  render: (row: T) => ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  rows: T[] | undefined;
  getRowId: (row: T) => string | number;
  loading?: boolean;
  /** Filas dadas de baja: se muestran atenuadas. */
  isInactive?: (row: T) => boolean;
  emptyTitle?: string;
  /** Por ejemplo, la paginación. */
  footer?: ReactNode;
}

/**
 * Tabla genérica: skeleton mientras carga, mensaje si no hay datos
 * y filas inactivas atenuadas. La paginación la resuelve el servidor.
 */
export function DataTable<T>({
  columns,
  rows,
  getRowId,
  loading = false,
  isInactive,
  emptyTitle = "No hay registros para mostrar",
  footer,
}: DataTableProps<T>) {
  const vacio = !loading && (rows?.length ?? 0) === 0;

  return (
    <div className="overflow-hidden rounded-xl border border-surface-border bg-surface">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-muted text-xs font-semibold tracking-wide text-navy-500 uppercase">
            <tr>
              {columns.map((col) => (
                <th
                  key={col.key}
                  scope="col"
                  className={cn("px-4 py-3", col.className)}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border">
            {loading && <SkeletonRows cols={columns.length} />}
            {!loading &&
              rows?.map((row) => (
                <tr
                  key={getRowId(row)}
                  className={cn(isInactive?.(row) && "opacity-60")}
                >
                  {columns.map((col) => (
                    <td
                      key={col.key}
                      className={cn("px-4 py-3", col.className)}
                    >
                      {col.render(row)}
                    </td>
                  ))}
                </tr>
              ))}
          </tbody>
        </table>
      </div>
      {vacio && <EstadoVacio titulo={emptyTitle} />}
      {footer}
    </div>
  );
}
