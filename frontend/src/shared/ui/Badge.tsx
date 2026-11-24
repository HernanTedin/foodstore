import type { ReactNode } from "react";

import { cn } from "@/shared/lib/cn";

type Tone = "neutral" | "accent" | "success" | "danger";

const tonos: Record<Tone, string> = {
  neutral: "bg-surface-muted text-navy-700 border-surface-border",
  accent: "bg-accent-100 text-navy-900 border-accent-100",
  success: "bg-green-50 text-green-800 border-green-100",
  danger: "bg-danger-50 text-red-800 border-red-100",
};

export function Badge({
  tone = "neutral",
  children,
}: {
  tone?: Tone;
  children: ReactNode;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium",
        tonos[tone],
      )}
    >
      {children}
    </span>
  );
}
