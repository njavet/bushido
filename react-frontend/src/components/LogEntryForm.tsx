import { useState, type FormEvent } from "react";
import { ApiError, logUnit } from "../api/client";
import type { LoggedUnit } from "../api/types";

export function LogEntryForm() {
  const [line, setLine] = useState("");
  const [result, setResult] = useState<LoggedUnit | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = line.trim();
    if (!trimmed) return;

    setPending(true);
    setError(null);
    try {
      const logged = await logUnit(trimmed);
      setResult(logged);
      setLine("");
    } catch (err) {
      setResult(null);
      setError(err instanceof ApiError ? err.message : "Could not reach the server");
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="log-entry">
      <h2>Log a session</h2>
      <form onSubmit={handleSubmit} className="log-entry__form">
        <span className="log-entry__prompt">&gt;</span>
        <input
          className="log-entry__input"
          value={line}
          onChange={(event) => setLine(event.target.value)}
          placeholder="squat 100 5 180 100 5 --dt 20260528-1800 # felt heavy"
          spellCheck={false}
          autoComplete="off"
        />
        <button type="submit" disabled={pending || !line.trim()}>
          {pending ? "Logging…" : "Log entry"}
        </button>
      </form>

      {result && (
        <p className="log-entry__receipt" role="status">
          <span className="log-entry__check">✓</span> Logged {result.unit_name} ({result.category}) at{" "}
          {new Date(result.logged_at).toLocaleString()}
        </p>
      )}
      {error && (
        <p className="log-entry__error" role="alert">
          {error}
        </p>
      )}
    </section>
  );
}