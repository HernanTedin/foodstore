import { useState } from "react";
import { useNavigate } from "react-router";

import { DataTable, type Column } from "@/shared/components/DataTable";
import { FilterBar, type EstadoFiltro } from "@/shared/components/FilterBar";
import { Paginacion } from "@/shared/components/Paginacion";
import { useUiStore } from "@/store/uiStore";
import { Badge } from "@/shared/ui/Badge";

import { UsuarioFormModal } from "../components/UsuarioFormModal";
import {
  mensajeError,
  useUsuariosMutations,
} from "../hooks/useUsuariosMutations";
import { useUsuarios } from "../hooks/useUsuarios";
import type { UsuarioAdmin } from "../types/usuarios";

const ROLES = [
  { value: "", label: "Todos los roles" },
  { value: "ADMIN", label: "Administrador" },
  { value: "STOCK", label: "Stock" },
  { value: "PEDIDOS", label: "Pedidos" },
  { value: "CLIENT", label: "Cliente" },
];

const BOTON =
  "rounded-md px-2 py-1 text-xs font-medium hover:bg-surface-muted focus-visible:ring-2 focus-visible:ring-accent-600 focus-visible:outline-none";

export default function UsuariosPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [rol, setRol] = useState("");
  const [estado, setEstado] = useState<EstadoFiltro>("activos");
  const [editando, setEditando] = useState<UsuarioAdmin | null>(null);

  const navigate = useNavigate();
  const openConfirm = useUiStore((s) => s.openConfirm);
  const { cambiarEstado, darDeBaja } = useUsuariosMutations();
  const { data, isLoading, isError } = useUsuarios({
    page,
    size: 10,
    search,
    rol,
    estado,
  });

  function exito(title: string, message: string) {
    navigate("/success", {
      state: { title, message, to: "/usuarios", cta: "Volver a usuarios" },
    });
  }

  function fallo(error: unknown) {
    navigate("/error", {
      state: {
        title: "No se pudo completar",
        message: mensajeError(error),
        to: "/usuarios",
        cta: "Volver a usuarios",
      },
    });
  }

  function confirmarEstado(u: UsuarioAdmin) {
    const bloquear = !u.disabled;
    openConfirm({
      title: bloquear ? "Bloquear usuario" : "Desbloquear usuario",
      message: bloquear
        ? `${u.nombre} ${u.apellido} va a perder el acceso en su próximo pedido.`
        : `${u.nombre} ${u.apellido} va a poder volver a ingresar.`,
      confirmLabel: bloquear ? "Bloquear" : "Desbloquear",
      tone: bloquear ? "danger" : "default",
      onConfirm: async () => {
        try {
          await cambiarEstado.mutateAsync({ id: u.id, disabled: bloquear });
          exito(
            bloquear ? "Usuario bloqueado" : "Usuario desbloqueado",
            `${u.nombre} ${u.apellido} fue ${bloquear ? "bloqueado" : "desbloqueado"}.`,
          );
        } catch (e) {
          fallo(e);
        }
      },
    });
  }

  function confirmarBaja(u: UsuarioAdmin) {
    openConfirm({
      title: "Dar de baja",
      message: `Vas a dar de baja a ${u.nombre} ${u.apellido}. Va a quedar como inactivo.`,
      confirmLabel: "Dar de baja",
      tone: "danger",
      onConfirm: async () => {
        try {
          await darDeBaja.mutateAsync(u.id);
          exito(
            "Usuario dado de baja",
            `${u.nombre} ${u.apellido} quedó inactivo.`,
          );
        } catch (e) {
          fallo(e);
        }
      },
    });
  }

  const columnas: Column<UsuarioAdmin>[] = [
    {
      key: "nombre",
      header: "Nombre",
      render: (u) => (
        <span className="font-medium text-navy-900">
          {u.nombre} {u.apellido}
        </span>
      ),
    },
    { key: "email", header: "Email", render: (u) => u.email },
    { key: "telefono", header: "Teléfono", render: (u) => u.telefono ?? "—" },
    {
      key: "roles",
      header: "Roles",
      render: (u) => (
        <div className="flex flex-wrap gap-1">
          {u.roles.map((r) => (
            <Badge key={r} tone="accent">
              {r}
            </Badge>
          ))}
        </div>
      ),
    },
    {
      key: "estado",
      header: "Estado",
      render: (u) =>
        u.deleted_at ? (
          <Badge tone="neutral">Inactivo</Badge>
        ) : u.disabled ? (
          <Badge tone="danger">Bloqueado</Badge>
        ) : (
          <Badge tone="success">Activo</Badge>
        ),
    },
    {
      key: "acciones",
      header: "Acciones",
      render: (u) =>
        u.deleted_at ? null : (
          <div className="flex flex-wrap gap-1">
            <button
              type="button"
              className={`${BOTON} text-navy-700`}
              onClick={() => setEditando(u)}
            >
              Editar
            </button>
            <button
              type="button"
              className={`${BOTON} text-navy-700`}
              onClick={() => confirmarEstado(u)}
            >
              {u.disabled ? "Desbloquear" : "Bloquear"}
            </button>
            <button
              type="button"
              className={`${BOTON} text-danger-600`}
              onClick={() => confirmarBaja(u)}
            >
              Dar de baja
            </button>
          </div>
        ),
    },
  ];

  return (
    <div className="flex flex-col gap-4 p-6">
      <h1 className="text-2xl font-bold text-navy-900">Usuarios</h1>

      <FilterBar
        search={search}
        onSearchChange={(v) => {
          setSearch(v);
          setPage(1);
        }}
        estado={estado}
        onEstadoChange={(v) => {
          setEstado(v);
          setPage(1);
        }}
        placeholder="Buscar por nombre, apellido o email…"
        extra={
          <select
            aria-label="Filtrar por rol"
            value={rol}
            onChange={(e) => {
              setRol(e.target.value);
              setPage(1);
            }}
            className="h-10 rounded-lg border border-surface-border bg-surface px-3 text-sm"
          >
            {ROLES.map((r) => (
              <option key={r.value} value={r.value}>
                {r.label}
              </option>
            ))}
          </select>
        }
      />

      {isError && (
        <p
          role="alert"
          className="rounded-lg bg-danger-50 px-3 py-2 text-sm text-red-800"
        >
          No pudimos cargar los usuarios.
        </p>
      )}

      <DataTable
        columns={columnas}
        rows={data?.items}
        getRowId={(u) => u.id}
        loading={isLoading}
        isInactive={(u) => u.deleted_at !== null}
        emptyTitle="No hay usuarios para mostrar"
        footer={
          data && (
            <Paginacion
              page={data.page}
              pages={data.pages}
              total={data.total}
              onChange={setPage}
            />
          )
        }
      />

      {editando && (
        <UsuarioFormModal
          key={editando.id}
          usuario={editando}
          onClose={() => setEditando(null)}
        />
      )}
    </div>
  );
}
