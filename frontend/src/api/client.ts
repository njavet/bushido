import type {
  LoadedUnits,
  LoadUnitRequest,
  LoggedUnit,
  LogUnitRequest,
  UnitSetting,
} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

function authHeaders(): HeadersInit {
  const token = localStorage.getItem("bushido_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(init?.headers ?? {}),
    },
  });

  if (!res.ok) {
    // FastAPI's default error body is {"detail": "..."} — surface it directly
    // rather than a generic "request failed" message.
    let detail = res.statusText;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") detail = body.detail;
    } catch {
      // response wasn't JSON — fall back to statusText
    }
    throw new ApiError(res.status, detail);
  }

  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}

export function getUnitSettings(): Promise<UnitSetting[]> {
  return request<UnitSetting[]>("/unit-settings");
}

export function logUnit(line: string): Promise<LoggedUnit> {
  const body: LogUnitRequest = { line };
  return request<LoggedUnit>("/unit-logs", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function queryUnits(filter: LoadUnitRequest): Promise<LoadedUnits> {
  return request<LoadedUnits>("/unit-logs/query", {
    method: "POST",
    body: JSON.stringify(filter),
  });
}