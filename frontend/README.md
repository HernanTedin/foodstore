# Food Store · Frontend

Interfaz web de Food Store, hecha con React 19, TypeScript, Vite y Tailwind CSS 4.

## Requisitos

- Node.js 20 o superior
- El backend corriendo en `http://127.0.0.1:8000` (ver el README de la raíz)

## Cómo correrlo

Desde esta carpeta (`frontend`):

```bash
npm install
npm run dev
```

La aplicación queda en `http://localhost:5173`. Las llamadas a `/api` y `/media` se redirigen solas al backend (configurado en `vite.config.ts`).

## Scripts

| Comando | Qué hace |
|---|---|
| `npm run dev` | Servidor de desarrollo |
| `npm run build` | Revisa los tipos y genera la versión para producción |
| `npm run preview` | Sirve la versión de producción generada |

## Estructura

```
src/
├── shared/    # Piezas reutilizables: api, componentes, layout, ui
├── features/  # Una carpeta por módulo (auth, usuarios, direcciones…)
├── store/     # Estado del cliente (Zustand)
├── routes/    # Rutas de la aplicación
├── pages/     # Páginas generales
└── styles/    # Estilos globales y colores
```

## Decisiones técnicas

- **Estado del servidor:** TanStack Query (listas, cachés y recargas).
- **Estado del cliente:** Zustand (sesión y modal de confirmación).
- **Sesión:** los tokens viajan en cookies HttpOnly; el frontend nunca los lee.
- **Confirmaciones y resultados:** modal propio y páginas `/success` y `/error`, sin `window.confirm` ni avisos flotantes.