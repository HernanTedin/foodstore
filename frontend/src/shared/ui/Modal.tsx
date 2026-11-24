import { useEffect, useRef, type ReactNode } from "react";

interface ModalProps {
  open: boolean;
  title: string;
  onClose: () => void;
  children: ReactNode;
  footer?: ReactNode;
}

/** Ventana modal basada en <dialog>: el foco y la tecla Escape ya vienen resueltos. */
export function Modal({ open, title, onClose, children, footer }: ModalProps) {
  const ref = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      onClose={onClose}
      aria-labelledby="modal-titulo"
      className="m-auto w-full max-w-md rounded-xl border border-surface-border bg-surface p-0 text-navy-900 shadow-xl backdrop:bg-navy-900/50"
    >
      <div className="p-6">
        <h2 id="modal-titulo" className="text-lg font-semibold">
          {title}
        </h2>
        <div className="mt-3 text-sm text-navy-700">{children}</div>
      </div>
      {footer && (
        <div className="flex justify-end gap-3 border-t border-surface-border px-6 py-4">
          {footer}
        </div>
      )}
    </dialog>
  );
}
