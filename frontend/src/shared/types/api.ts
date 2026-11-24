export type RolCodigo = "ADMIN" | "STOCK" | "PEDIDOS" | "CLIENT";

export interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  telefono: string | null;
  roles: RolCodigo[];
}

/** Formato estándar de error de la API: { detail, code, field }. */
export interface ApiError {
  detail: string;
  code: string;
  field: string | null;
}
/** Respuesta paginada: ?page=1&size=20 → { items, total, page, size, pages } */
export interface Paginated<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
