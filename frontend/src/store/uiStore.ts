import { create } from "zustand";

/** Datos de una confirmación pendiente: qué preguntar y qué hacer si acepta. */
export interface ConfirmOptions {
  title: string;
  message: string;
  confirmLabel?: string;
  tone?: "default" | "danger";
  onConfirm: () => void | Promise<void>;
}

interface UiState {
  confirm: ConfirmOptions | null;
  openConfirm: (options: ConfirmOptions) => void;
  closeConfirm: () => void;
}

export const useUiStore = create<UiState>()((set) => ({
  confirm: null,
  openConfirm: (confirm) => set({ confirm }),
  closeConfirm: () => set({ confirm: null }),
}));
