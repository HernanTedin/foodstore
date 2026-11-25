export interface Direccion {
  id: number;
  alias: string | null;
  linea1: string;
  linea2: string | null;
  ciudad: string | null;
  provincia: string | null;
  codigo_postal: string | null;
  lat: number | null;
  lng: number | null;
  es_principal: boolean;
  created_at: string;
}

/** Lo que se manda al crear o editar (la principal se maneja aparte al editar). */
export interface DireccionInput {
  alias: string | null;
  linea1: string;
  linea2: string | null;
  ciudad: string | null;
  provincia: string | null;
  codigo_postal: string | null;
  lat: number | null;
  lng: number | null;
}
