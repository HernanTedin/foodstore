import { useState } from "react";
import { useNavigate } from "react-router";

import { EstadoVacio } from "@/shared/components/EstadoVacio";
import { Skeleton } from "@/shared/components/Skeleton";
import { mensajeError } from "@/shared/lib/mensajeError";
import { Badge } from "@/shared/ui/Badge";
import { useUiStore } from "@/store/uiStore";

import { DireccionFormModal } from "../components/DireccionFormModal";
import {
  useDirecciones,
  useDireccionesMutations,
} from "../hooks/useDirecciones";
import type { Direccion } from "../types/direcciones";

const BOTON =
  "rounded-md px-2 py-1 text-xs font-medium hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent-600 focus-visible:outline-none";

export default function DireccionesPage() {
  // undefined = modal cerrado, null = crear, Direccion = editar
  const [editando, setEditando] = useState<Direccion | null | undefined>(
    undefined,
  );

  const navigate = useNavigate();
  const openConfirm = useUiStore((s) => s.openConfirm);
  const { marcarPrincipal, eliminar } = useDireccionesMutations();
  const { data, isLoading, isError } = useDirecciones();

  function resultado(ok: boolean, title: string, message: string) {
    navigate(ok ? "/success" : "/error", {
      state: {
        title,
        message,
        to: "/direcciones",
        cta: "Volver a mis direcciones",
      },
    });
  }

  async function hacerPrincipal(d: Direccion) {
    try {
      await marcarPrincipal.mutateAsync(d.id);
      resultado(
        true,
        "Dirección principal actualizada",
        `${d.alias ?? d.linea1} es ahora tu dirección principal.`,
      );
    } catch (e) {
      resultado(false, "No se pudo completar", mensajeError(e));
    }
  }

  function confirmarEliminar(d: Direccion) {
    openConfirm({
      title: "Eliminar dirección",
      message: `Vas a eliminar "${d.alias ?? d.linea1}".`,
      confirmLabel: "Eliminar",
      tone: "danger",
      onConfirm: async () => {
        try {
          await eliminar.mutateAsync(d.id);
          resultado(
            true,
            "Dirección eliminada",
            "La dirección se eliminó correctamente.",
          );
        } catch (e) {
          resultado(false, "No se pudo completar", mensajeError(e));
        }
      },
    });
  }

  return (
    <div className="flex flex-col gap-4 p-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-navy-900">Mis direcciones</h1>
        <button
          type="button"
          onClick={() => setEditando(null)}
          className="h-10 rounded-lg bg-accent-600 px-4 text-sm font-semibold text-white hover:bg-accent-700"
        >
          Nueva dirección
        </button>
      </div>

      {isError && (
        <p
          role="alert"
          className="rounded-lg bg-danger-50 px-3 py-2 text-sm text-red-800"
        >
          No pudimos cargar tus direcciones.
        </p>
      )}

      {isLoading && (
        <div className="flex flex-col gap-3">
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-24 w-full" />
        </div>
      )}

      {data && data.length === 0 && (
        <div className="rounded-xl border border-surface-border bg-surface">
          <EstadoVacio
            titulo="Todavía no cargaste direcciones"
            descripcion="Agregá una para poder recibir tus pedidos."
          />
        </div>
      )}

      <ul className="flex flex-col gap-3">
        {data?.map((d) => (
          <li
            key={d.id}
            className="flex flex-col gap-3 rounded-xl border border-surface-border bg-surface p-4 sm:flex-row sm:items-center sm:justify-between"
          >
            <div>
              <div className="flex items-center gap-2">
                <p className="font-semibold text-navy-900">
                  {d.alias ?? d.linea1}
                </p>
                {d.es_principal && <Badge tone="accent">Principal</Badge>}
              </div>
              <p className="text-sm text-navy-700">
                {d.linea1}
                {d.linea2 ? `, ${d.linea2}` : ""}
              </p>
              <p className="text-sm text-navy-500">
                {[d.ciudad, d.provincia, d.codigo_postal]
                  .filter(Boolean)
                  .join(" · ")}
              </p>
            </div>
            <div className="flex flex-wrap gap-1">
              <button
                type="button"
                className={`${BOTON} text-navy-700`}
                onClick={() => setEditando(d)}
              >
                Editar
              </button>
              {!d.es_principal && (
                <button
                  type="button"
                  className={`${BOTON} text-navy-700`}
                  onClick={() => hacerPrincipal(d)}
                >
                  Marcar como principal
                </button>
              )}
              <button
                type="button"
                className={`${BOTON} text-danger-600`}
                onClick={() => confirmarEliminar(d)}
              >
                Eliminar
              </button>
            </div>
          </li>
        ))}
      </ul>

      {editando !== undefined && (
        <DireccionFormModal
          key={editando?.id ?? "nueva"}
          direccion={editando}
          onClose={() => setEditando(undefined)}
        />
      )}
    </div>
  );
}
