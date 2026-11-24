import type { ReactNode } from "react";

export function EstadoVacio({
  titulo,
  descripcion,
  accion,
}: {
  titulo: string;
  descripcion?: string;
  accion?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 px-6 py-12 text-center">
      <p className="text-base font-semibold text-navy-900">{titulo}</p>
      {descripcion && (
        <p className="max-w-sm text-sm text-navy-500">{descripcion}</p>
      )}
      {accion && <div className="mt-3">{accion}</div>}
    </div>
  );
}
