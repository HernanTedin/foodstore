import { QueryClient } from "@tanstack/react-query";

/** Instancia única de TanStack Query (estado del servidor). */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30_000, refetchOnWindowFocus: false, retry: false },
    mutations: { retry: false },
  },
});
