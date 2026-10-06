import { useEffect, useState } from "react";
import { ApiError, getUnitSettings } from "../api/client";
import type { UnitSetting } from "../api/types";

export function UnitSettingsPanel() {
  const [units, setUnits] = useState<UnitSetting[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getUnitSettings()
      .then(setUnits)
      .catch((err) =>
        setError(err instanceof ApiError ? err.message : "Could not load units")
      );
  }, []);

  return (
    <section className="unit-settings">
      <h2>Known units</h2>
      {error && (
        <p className="log-entry__error" role="alert">
          {error}
        </p>
      )}
      {!units && !error && <p className="unit-settings__muted">Loading…</p>}
      {units && units.length === 0 && (
        <p className="unit-settings__muted">No units registered yet.</p>
      )}
      {units && units.length > 0 && (
        <ul className="unit-settings__list">
          {units.map((unit) => (
            <li key={unit.unit_name}>
              <span className="unit-settings__name">{unit.unit_name}</span>
              <span className="unit-settings__category">{unit.category}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}