export async function parseCSV(filePath: string): Promise<Record<string, string>[]> {
  const response = await fetch(filePath);
  if (!response.ok) {
    throw new Error(`Não foi possível carregar o CSV: ${response.status}`);
  }

  const rows = (await response.text())
    .trim()
    .split(/\r?\n/)
    .filter(Boolean)
    .map((row) => row.split(',').map((value) => value.trim().replace(/^"|"$/g, '')));

  const headers = rows.shift() ?? [];
  return rows.map((values) => Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ''])));
}
