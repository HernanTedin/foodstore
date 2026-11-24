import type { ReactNode } from "react";

import { Header } from "@/shared/layout/Header";
import { Sidebar } from "@/shared/layout/Sidebar";
import { ConfirmModal } from "@/shared/ui/ConfirmModal";
export function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-surface-muted">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header />
        <main className="flex-1 p-6">{children}</main>
        <ConfirmModal />
      </div>
    </div>
  );
}
