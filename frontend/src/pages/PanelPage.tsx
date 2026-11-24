import { AppLayout } from "@/shared/layout/AppLayout";
// import { ROL_NOMBRE } from "@/shared/layout/navigation";
import { useAuthStore } from "@/store/authStore";

// const FASES = [
//   { nombre: "Fase 0 · Fundamentos", estado: "En curso" },
//   { nombre: "Fase 1 · Usuarios y ABM", estado: "Pendiente" },
//   { nombre: "Fase 2 · Catálogo", estado: "Pendiente" },
//   { nombre: "Fase 3 · Inventario y producción", estado: "Pendiente" },
//   { nombre: "Fase 4 · Pedidos y pagos", estado: "Pendiente" },
//   { nombre: "Fase 5 · Métricas", estado: "Pendiente" },
//   { nombre: "Fase 6 · Cierre", estado: "Pendiente" },
// ];

export default function PanelPage() {
  const usuario = useAuthStore((s) => s.usuario);

  return (
    <AppLayout>
      <h1 className="text-2xl font-bold text-navy-900">
        Hola, {usuario?.nombre} 👋
      </h1>
      <p className="mt-1 text-navy-500">Bienvenido a Food Store.</p>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <section className="rounded-xl border border-surface-border bg-surface p-5">
          <h2 className="font-semibold text-navy-900">Tu cuenta</h2>
          <dl className="mt-3 space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-navy-500">Email</dt>
              <dd className="text-navy-900">{usuario?.email}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-navy-500">Teléfono</dt>
              <dd className="text-navy-900">{usuario?.telefono ?? "—"}</dd>
            </div>
          </dl>
        </section>
      </div>
    </AppLayout>
  );
}
