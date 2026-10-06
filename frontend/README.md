# Bushido Web

Minimal Elm frontend for Citadel.

## Development

Install Elm:

```bash
sudo pacman -S elm
```

Build:

```bash
elm make src/Main.elm --output=elm.js
```

Serve the static files:

```bash
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

Citadel is expected at:

```text
http://localhost:8000
```

Change `apiBaseUrl` in `index.html` for another backend.

## Commands

```text
log <unit line>
load <unit_name>
```

Examples:

```text
log squat 120 100 5
load squat
```

`load` currently sends:

```json
{
  "unit_name": "squat",
  "start_t": null,
  "end_t": null
}
```

The raw `LoggedUnit` JSON is retained and rendered generically in v1. This deliberately avoids duplicating the complete Citadel discriminated union in Elm before type-specific tables are implemented.
