import { api } from "@/shared/api/axiosInstance";

import type { Direccion, DireccionInput } from "../types/direcciones";

export const direccionesApi = {
  async listar(): Promise<Direccion[]> {
    const { data } = await api.get<Direccion[]>("/direcciones");
    return data;
  },

  async crear(
    datos: DireccionInput & { es_principal: boolean },
  ): Promise<Direccion> {
    const { data } = await api.post<Direccion>("/direcciones", datos);
    return data;
  },

  async actualizar(id: number, datos: DireccionInput): Promise<Direccion> {
    const { data } = await api.put<Direccion>(`/direcciones/${id}`, datos);
    return data;
  },

  async marcarPrincipal(id: number): Promise<Direccion> {
    const { data } = await api.patch<Direccion>(`/direcciones/${id}/principal`);
    return data;
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/direcciones/${id}`);
  },
};
