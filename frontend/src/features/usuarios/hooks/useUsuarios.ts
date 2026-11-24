import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { usuariosApi } from "../api/usuariosApi";
import type { UsuariosFiltros } from "../types/usuarios";

/** Trae la lista de usuarios. Si cambia un filtro, vuelve a pedir al servidor. */
export function useUsuarios(filtros: UsuariosFiltros) {
  return useQuery({
    queryKey: ["usuarios", filtros],
    queryFn: () => usuariosApi.listar(filtros),
    placeholderData: keepPreviousData,
  });
}
