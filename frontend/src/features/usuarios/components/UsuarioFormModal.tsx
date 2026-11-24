import { useState } from "react";

import { EntityFormModal } from "@/shared/components/EntityFormModal";
import type { RolCodigo } from "@/shared/types/api";
import { Input } from "@/shared/ui/Input";

import {
  mensajeError,
  useUsuariosMutations,
} from "../hooks/useUsuariosMutations";
import type { UsuarioAdmin } from "../types/usuarios";

const ROLES: { value: RolCodigo; label: string }[] = [
  { value: "ADMIN", label: "Administrador" },
  { value: "STOCK", label: "Stock" },
  { value: "PEDIDOS", label: "Pedidos" },
  { value: "CLIENT", label: "Cliente" },
];

interface Props {
  usuario: UsuarioAdmin;
  onClose: () => void;
}

/** Edita datos y roles. Se monta solo mientras está abierto, así siempre arranca limpio. */
export function UsuarioFormModal({ usuario, onClose }: Props) {
  const { guardar } = useUsuariosMutations();
  const [nombre, setNombre] = useState(usuario.nombre);
  const [apellido, setApellido] = useState(usuario.apellido);
  const [telefono, setTelefono] = useState(usuario.telefono ?? "");
  const [roles, setRoles] = useState<RolCodigo[]>(usuario.roles);
  const [error, setError] = useState<string | null>(null);

  function alternarRol(rol: RolCodigo) {
    setRoles((actuales) =>
      actuales.includes(rol)
        ? actuales.filter((r) => r !== rol)
        : [...actuales, rol],
    );
  }

  function enviar() {
    if (!nombre.trim() || !apellido.trim()) {
      setError("El nombre y el apellido son obligatorios.");
      return;
    }
    if (roles.length === 0) {
      setError("El usuario tiene que tener al menos un rol.");
      return;
    }
    setError(null);
    guardar.mutate(
      {
        id: usuario.id,
        nombre: nombre.trim(),
        apellido: apellido.trim(),
        telefono: telefono.trim() || null,
        roles,
      },
      { onSuccess: onClose, onError: (e) => setError(mensajeError(e)) },
    );
  }

  return (
    <EntityFormModal
      open
      mode="edicion"
      entityName="usuario"
      submitting={guardar.isPending}
      error={error}
      onClose={onClose}
      onSubmit={enviar}
    >
      <Input
        label="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <Input
        label="Apellido"
        value={apellido}
        onChange={(e) => setApellido(e.target.value)}
      />
      <Input
        label="Teléfono"
        value={telefono}
        onChange={(e) => setTelefono(e.target.value)}
      />
      <Input
        label="Email"
        value={usuario.email}
        disabled
        hint="El email no se puede cambiar."
      />

      <fieldset className="flex flex-col gap-2">
        <legend className="text-sm font-medium text-navy-900">Roles</legend>
        {ROLES.map((r) => (
          <label
            key={r.value}
            className="flex items-center gap-2 text-sm text-navy-700"
          >
            <input
              type="checkbox"
              checked={roles.includes(r.value)}
              onChange={() => alternarRol(r.value)}
            />
            {r.label}
          </label>
        ))}
      </fieldset>
    </EntityFormModal>
  );
}
