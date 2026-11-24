/** Misma política que el backend. Devuelve los requisitos que faltan. */
export function requisitosPendientes(password: string): string[] {
  const faltan: string[] = [];
  if (password.length < 12) faltan.push("12 caracteres");
  if (!/[A-Z]/.test(password)) faltan.push("una mayúscula");
  if (!/\d/.test(password)) faltan.push("un dígito");
  if (!/[^A-Za-z0-9]/.test(password)) faltan.push("un carácter especial");
  return faltan;
}
