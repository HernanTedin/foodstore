import { api } from "@/shared/api/axiosInstance";
import type { Paginated, RolCodigo } from "@/shared/types/api";

import type { UsuarioAdmin, UsuariosFiltros } from "../types/usuarios";

export const usuariosApi = {
  async listar(f: UsuariosFiltros): Promise<Paginated<UsuarioAdmin>> {
    const { data } = await api.get<Paginated<UsuarioAdmin>>("/usuarios", {
      params: {
        page: f.page,
        size: f.size,
        search: f.search || undefined,
        rol: f.rol || undefined,
        incluir_inactivos: f.estado === "todos" || undefined,
        solo_inactivos: f.estado === "inactivos" || undefined,
      },
    });
    return data;
  },

  async actualizar(
    id: number,
    datos: { nombre: string; apellido: string; telefono: string | null },
  ): Promise<UsuarioAdmin> {
    const { data } = await api.put<UsuarioAdmin>(`/usuarios/${id}`, datos);
    return data;
  },

  async cambiarRoles(id: number, roles: RolCodigo[]): Promise<UsuarioAdmin> {
    const { data } = await api.put<UsuarioAdmin>(`/usuarios/${id}/roles`, {
      roles,
    });
    return data;
  },

  async cambiarEstado(id: number, disabled: boolean): Promise<UsuarioAdmin> {
    const { data } = await api.patch<UsuarioAdmin>(`/usuarios/${id}/estado`, {
      disabled,
    });
    return data;
  },

  async darDeBaja(id: number): Promise<void> {
    await api.delete(`/usuarios/${id}`);
  },
};
