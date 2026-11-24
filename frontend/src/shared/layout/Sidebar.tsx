import { NAV } from "@/shared/layout/navigation";
import { useAuthStore } from "@/store/authStore";

export function Sidebar() {
  const hasRole = useAuthStore((s) => s.hasRole);
  const items = NAV.filter((item) => hasRole(...item.roles));

  return (
    <aside className="hidden w-60 shrink-0 flex-col bg-navy-900 p-4 md:flex">
      <p className="mb-6 px-2 text-xl font-bold text-white">
        Food <span className="text-accent-600">Store</span>
      </p>
      <nav className="space-y-1">
        {items.map((item) =>
          item.disponible ? (
            <a
              key={item.to}
              href={item.to}
              className="flex items-center rounded-lg bg-navy-800 px-3 py-2 text-sm font-medium text-white"
            >
              {item.label}
            </a>
          ) : (
            <span
              key={item.to}
              className="flex items-center justify-between rounded-lg px-3 py-2 text-sm text-navy-300 opacity-60"
            >
              {item.label}
              <span className="rounded bg-navy-700 px-1.5 py-0.5 text-[10px] uppercase">
                Pronto
              </span>
            </span>
          ),
        )}
      </nav>
    </aside>
  );
}
