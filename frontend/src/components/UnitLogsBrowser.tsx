import { useState, type FormEvent } from "react";
import { ApiError, queryUnits } from "../api/client";
import type { LoadedUnits, LoadUnitRequest } from "../api/types";

const EMPTY_FILTER: LoadUnitRequest = {};

export function UnitLogsBrowser() {
  const [filter, setFilter] = useState<LoadUnitRequest>(EMPTY_FILTER);
  const [result, setResult] = useState<LoadedUnits | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      setResult(await queryUnits(filter));
    } catch (err) {
      setResult(null);
      setError(err instanceof ApiError ? err.message : "Could not reach the server");
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="unit-logs">
      <h2>Browse entries</h2>
      <form onSubmit={handleSubmit} className="unit-logs__filters">
        <input
          placeholder="unit name"
          value={filter.unit_name ?? ""}
          onChange={(event) =>
            setFilter({ ...filter, unit_name: event.target.value || undefined })
          }
        />
        <input
          placeholder="category"
          value={filter.category ?? ""}
          onChange={(event) =>
            setFilter({ ...filter, category: event.target.value || undefined })
          }
        />
        <button type="submit" disabled={pending}>
          {pending ? "Searching…" : "Search"}
        </button>
      </form>

      {error && (
        <p className="log-entry__error" role="alert">
          {error}
        </p>
      )}

      {result && result.entries.length > 0 && (
        <table className="unit-logs__table">
          <thead>
            <tr>
              <th>Logged</th>
              <th>Unit</th>
              <th>Category</th>
              <th>Comment</th>
            </tr>
          </thead>
          <tbody>
            {result.entries.map((entry) => (
              <tr key={entry.id}>
                <td>{new Date(entry.logged_at).toLocaleString()}</td>
                <td>{entry.unit_name}</td>
                <td>{entry.category}</td>
                <td>{entry.comment ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {result && result.entries.length === 0 && (
        <p className="unit-logs__empty">No entries match yet.</p>
      )}
    </section>
  );
}