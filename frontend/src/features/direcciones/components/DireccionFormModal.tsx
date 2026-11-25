import { useState } from "react";

import { EntityFormModal } from "@/shared/components/EntityFormModal";
import { mensajeError } from "@/shared/lib/mensajeError";
import { Input } from "@/shared/ui/Input";

import { useDireccionesMutations } from "../hooks/useDirecciones";
import type { Direccion } from "../types/direcciones";

interface Props {
  /** null = crear una nueva; con datos = editar. */
  direccion: Direccion | null;
  onClose: () => void;
}

export function DireccionFormModal({ direccion, onClose }: Props) {
  const { guardar } = useDireccionesMutations();
  const [alias, setAlias] = useState(direccion?.alias ?? "");
  const [linea1, setLinea1] = useState(direccion?.linea1 ?? "");
  const [linea2, setLinea2] = useState(direccion?.linea2 ?? "");
  const [ciudad, setCiudad] = useState(direccion?.ciudad ?? "");
  const [provincia, setProvincia] = useState(direccion?.provincia ?? "");
  const [codigoPostal, setCodigoPostal] = useState(
    direccion?.codigo_postal ?? "",
  );

  const [principal, setPrincipal] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function enviar() {
    if (!linea1.trim()) {
      setError("La dirección (calle y número) es obligatoria.");
      return;
    }

    setError(null);
    guardar.mutate(
      {
        id: direccion?.id,
        es_principal: principal,
        datos: {
          alias: alias.trim() || null,
          linea1: linea1.trim(),
          linea2: linea2.trim() || null,
          ciudad: ciudad.trim() || null,
          provincia: provincia.trim() || null,
          codigo_postal: codigoPostal.trim() || null,
          lat: direccion?.lat ?? null,
          lng: direccion?.lng ?? null,
        },
      },
      { onSuccess: onClose, onError: (e) => setError(mensajeError(e)) },
    );
  }

  return (
    <EntityFormModal
      open
      mode={direccion ? "edicion" : "alta"}
      entityName="dirección"
      submitting={guardar.isPending}
      error={error}
      onClose={onClose}
      onSubmit={enviar}
    >
      <Input
        label="Alias"
        value={alias}
        onChange={(e) => setAlias(e.target.value)}
        hint="Por ejemplo: Casa, Trabajo."
      />
      <Input
        label="Calle y número"
        value={linea1}
        onChange={(e) => setLinea1(e.target.value)}
      />
      <Input
        label="Piso, depto u otros datos"
        value={linea2}
        onChange={(e) => setLinea2(e.target.value)}
      />
      <Input
        label="Ciudad"
        value={ciudad}
        onChange={(e) => setCiudad(e.target.value)}
      />
      <Input
        label="Provincia"
        value={provincia}
        onChange={(e) => setProvincia(e.target.value)}
      />
      <Input
        label="Código postal"
        value={codigoPostal}
        onChange={(e) => setCodigoPostal(e.target.value)}
      />

      {!direccion && (
        <label className="flex items-center gap-2 text-sm text-navy-700">
          <input
            type="checkbox"
            checked={principal}
            onChange={(e) => setPrincipal(e.target.checked)}
          />
          Usar como dirección principal
        </label>
      )}
    </EntityFormModal>
  );
}
