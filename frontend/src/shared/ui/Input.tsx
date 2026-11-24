import { useId, type InputHTMLAttributes } from "react";

import { cn } from "@/shared/lib/cn";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string | null;
  hint?: string;
}

export function Input({
  label,
  error,
  hint,
  className,
  id,
  ...rest
}: InputProps) {
  const autoId = useId();
  const inputId = id ?? autoId;
  const ayudaId = `${inputId}-ayuda`;

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={inputId} className="text-sm font-medium text-navy-900">
        {label}
      </label>
      <input
        id={inputId}
        aria-invalid={Boolean(error) || undefined}
        aria-describedby={error || hint ? ayudaId : undefined}
        className={cn(
          "h-10 rounded-lg border bg-surface px-3 text-sm text-navy-900 placeholder:text-navy-500",
          "focus-visible:ring-2 focus-visible:ring-accent-600 focus-visible:outline-none",
          error ? "border-danger-600" : "border-surface-border",
          className,
        )}
        {...rest}
      />
      {(error || hint) && (
        <p
          id={ayudaId}
          className={cn("text-xs", error ? "text-danger-600" : "text-navy-500")}
        >
          {error ?? hint}
        </p>
      )}
    </div>
  );
}
