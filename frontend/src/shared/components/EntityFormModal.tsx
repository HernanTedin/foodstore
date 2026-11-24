import type { FormEvent, ReactNode } from "react";

import { Modal } from "@/shared/ui/Modal";

interface EntityFormModalProps {
  open: boolean;
  /** 'alta' para crear, 'edicion' para editar: el mismo formulario sirve para los dos. */
  mode: "alta" | "edicion";
  entityName: string;
  submitting?: boolean;
  error?: string | null;
  onClose: () => void;
  onSubmit: () => void;
  children: ReactNode;
}

export function EntityFormModal({
  open,
  mode,
  entityName,
  submitting = false,
  error,
  onClose,
  onSubmit,
  children,
}: EntityFormModalProps) {
  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    onSubmit();
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={mode === "alta" ? `Nuevo ${entityName}` : `Editar ${entityName}`}
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
        {children}
        {error && (
          <p
            role="alert"
            className="rounded-lg bg-danger-50 px-3 py-2 text-sm text-red-800"
          >
            {error}
          </p>
        )}
        <div className="flex justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            disabled={submitting}
            className="h-10 rounded-lg border border-surface-border bg-surface px-4 text-sm text-navy-900 hover:bg-surface-muted disabled:opacity-60"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="h-10 rounded-lg bg-accent-600 px-4 text-sm font-semibold text-white hover:bg-accent-700 disabled:opacity-60"
          >
            {submitting
              ? "Guardando…"
              : mode === "alta"
                ? "Crear"
                : "Guardar cambios"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
