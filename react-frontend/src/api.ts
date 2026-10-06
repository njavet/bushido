const API_URL =
  import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function logUnit(line: string): Promise<unknown> {
  const response = await fetch(`${API_URL}/api/unit-logs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ line }),
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `HTTP ${response.status}`);
  }

  return response.json();
}
