import { isAxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { RolCodigo } from "@/shared/types/api";

import { usuariosApi } from "../api/usuariosApi";

/** Saca el mensaje de error que mandó el backend ({detail, code, field}). */
export function mensajeError(error: unknown): string {
  if (isAxiosError(error) && typeof error.response?.data?.detail === "string") {
    return error.response.data.detail;
  }
  return "No pudimos completar la operación. Probá de nuevo.";
}

/** Acciones de escritura. Después de cada una se vuelve a pedir la lista. */
export function useUsuariosMutations() {
  const queryClient = useQueryClient();
  const refrescar = () =>
    queryClient.invalidateQueries({ queryKey: ["usuarios"] });

  const guardar = useMutation({
    mutationFn: async (v: {
      id: number;
      nombre: string;
      apellido: string;
      telefono: string | null;
      roles: RolCodigo[];
    }) => {
      await usuariosApi.actualizar(v.id, {
        nombre: v.nombre,
        apellido: v.apellido,
        telefono: v.telefono,
      });
      await usuariosApi.cambiarRoles(v.id, v.roles);
    },
    onSuccess: refrescar,
  });

  const cambiarEstado = useMutation({
    mutationFn: (v: { id: number; disabled: boolean }) =>
      usuariosApi.cambiarEstado(v.id, v.disabled),
    onSuccess: refrescar,
  });

  const darDeBaja = useMutation({
    mutationFn: (id: number) => usuariosApi.darDeBaja(id),
    onSuccess: refrescar,
  });

  return { guardar, cambiarEstado, darDeBaja };
}
