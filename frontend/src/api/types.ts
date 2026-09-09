/**
 * Types mirroring the FastAPI schemas. `LogUnitRequest` is confirmed exactly
 * from the route handler (`log_unit(request.line, session)`); the rest are
 * best-guess shapes based on the earlier parsing-engine design — adjust the
 * fields here to match your actual Pydantic response_model definitions.
 */

export interface UnitSetting {
  unit_name: string;
  category: string;
  local_flags?: string[];
}

export interface LogUnitRequest {
  line: string;
}

export interface LoggedUnit {
  id: number;
  unit_name: string;
  category: string;
  logged_at: string; // ISO 8601
  payload: Record<string, unknown>;
  comment?: string | null;
}

export interface LoadUnitRequest {
  unit_name?: string;
  category?: string;
  from_dt?: string;
  to_dt?: string;
  limit?: number;
}

export interface LoadedUnits {
  entries: LoggedUnit[];
  total: number;
}