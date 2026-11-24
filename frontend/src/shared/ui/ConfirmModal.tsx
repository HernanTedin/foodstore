import { useState } from "react";

import { useUiStore } from "@/store/uiStore";
import { Modal } from "@/shared/ui/Modal";

/** Modal de confirmación global. Se monta una sola vez en el layout. */
export function ConfirmModal() {
  const confirm = useUiStore((s) => s.confirm);

  const closeConfirm = useUiStore((s) => s.closeConfirm);
  const [enviando, setEnviando] = useState(false);

  async function aceptar() {
    if (!confirm) return;
    setEnviando(true);
    try {
      await confirm.onConfirm();
    } finally {
      setEnviando(false);
      closeConfirm();
    }
  }

  const peligro = confirm?.tone === "danger";

  return (
    <Modal
      open={confirm !== null}
      title={confirm?.title ?? ""}
      onClose={closeConfirm}
      footer={
        <>
          <button
            type="button"
            onClick={closeConfirm}
            disabled={enviando}
            className="h-10 rounded-lg border border-surface-border bg-surface px-4 text-sm text-navy-900 hover:bg-surface-muted disabled:opacity-60"
          >
            Cancelar
          </button>
          <button
            type="button"
            onClick={aceptar}
            disabled={enviando}
            className={`h-10 rounded-lg px-4 text-sm font-semibold text-white disabled:opacity-60 ${
              peligro
                ? "bg-danger-600 hover:bg-red-700"
                : "bg-accent-600 hover:bg-accent-700"
            }`}
          >
            {enviando ? "Procesando…" : (confirm?.confirmLabel ?? "Confirmar")}
          </button>
        </>
      }
    >
      {confirm?.message}
    </Modal>
  );
}
