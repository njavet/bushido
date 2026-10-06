import { FormEvent, useState } from "react";

import { logUnit } from "./api";

export default function App() {
  const [line, setLine] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const value = line.trim();
    if (!value) {
      return;
    }

    try {
      setError(null);
      await logUnit(value);
      setLine("");
    } catch (error) {
      setError(error instanceof Error ? error.message : "Request failed");
    }
  }

  return (
    <main>
      <form onSubmit={submit}>
        <input
          autoFocus
          value={line}
          onChange={(event) => setLine(event.target.value)}
          placeholder="Enter unit..."
          aria-label="Unit"
        />
      </form>

      {error && <p>{error}</p>}
    </main>
  );
}
