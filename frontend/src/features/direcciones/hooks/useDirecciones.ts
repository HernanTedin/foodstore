import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { direccionesApi } from "../api/direccionesApi";
import type { DireccionInput } from "../types/direcciones";

export function useDirecciones() {
  return useQuery({
    queryKey: ["direcciones"],
    queryFn: direccionesApi.listar,
  });
}

/** Acciones de escritura. Después de cada una se vuelve a pedir la lista. */
export function useDireccionesMutations() {
  const queryClient = useQueryClient();
  const refrescar = () =>
    queryClient.invalidateQueries({ queryKey: ["direcciones"] });

  const guardar = useMutation({
    mutationFn: (v: {
      id?: number;
      datos: DireccionInput;
      es_principal: boolean;
    }) =>
      v.id === undefined
        ? direccionesApi.crear({ ...v.datos, es_principal: v.es_principal })
        : direccionesApi.actualizar(v.id, v.datos),
    onSuccess: refrescar,
  });

  const marcarPrincipal = useMutation({
    mutationFn: (id: number) => direccionesApi.marcarPrincipal(id),
    onSuccess: refrescar,
  });

  const eliminar = useMutation({
    mutationFn: (id: number) => direccionesApi.eliminar(id),
    onSuccess: refrescar,
  });

  return { guardar, marcarPrincipal, eliminar };
}
