# Bushido Web UI

## 1. Goal

Bushido Web is a minimal Elm client for Citadel.

It has two modes:

```text
UNAUTHENTICATED -> authentication terminal
AUTHENTICATED   -> Bushido command terminal
```

The initial version supports:

- signup
- login
- current-user lookup
- logout
- `log`
- `load`
- structured display of returned units
- API and authentication errors

The UI is intentionally small. No dashboard, charts, administration UI, frontend routing, or general shell is part of v1.

---

## 2. Architecture

```text
Browser
   |
   | static HTML/CSS/JS
   v
Bushido Elm frontend
   |
   | HTTPS / JSON / Bearer JWT
   v
Citadel / FastAPI
   |
   v
PostgreSQL
```

Production target:

```text
bushido.nj-cyb.org
        |
        v
static frontend hosting

api.bushido.nj-cyb.org
        |
        v
Azure Container Apps
        |
        v
Citadel
```

Elm executes in the browser.

Citadel remains the authority for:

- authentication
- authorization
- unit parsing
- unit validation
- Spartan ownership
- persistence

---

## 3. Visual design

Style:

- cyberpunk
- hacker terminal
- minimal science-fiction computer interface
- near-black background
- monospace typography
- restrained green/cyan accents
- thin borders
- subtle glow
- small system/status indicators
- no conventional SaaS dashboard aesthetic
- no large decorative illustrations
- no frontend framework/component-library appearance

The interface should resemble a functional terminal rather than a fake movie terminal.

Example:

```text
┌──────────────────────────────────────────────────────────┐
│ BUSHIDO // CITADEL                         ONLINE [●]    │
│ SPARTAN // NJ                                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  > log squat 120 100 5                                   │
│                                                          │
│  [OK] UNIT LOGGED                                        │
│  squat                                                   │
│  2026-10-06T08:31:17Z                                    │
│  ...                                                     │
│                                                          │
│  > load squat                                            │
│                                                          │
│  [OK] 14 RECORDS                                         │
│  ...                                                     │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ bushido> █                                               │
└──────────────────────────────────────────────────────────┘
```

Desktop is the primary target, but the application must remain usable on mobile.

---

## 4. API

All current endpoints have the `/api` prefix.

### Authentication

```text
POST /api/auth/signup
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/change-password
```

### Units

```text
GET  /api/unit/names
POST /api/unit/logs
POST /api/unit/logs/query
```

The frontend must not invent alternative REST endpoints.

---

## 5. Authentication state

Elm models authentication explicitly.

Conceptually:

```elm
type AuthState
    = LoggedOut
    | Authenticating
    | LoadingIdentity
    | LoggedIn Spartan
    | AuthFailed String
```

The main terminal cannot be displayed as authenticated merely because a token string exists.

The current Spartan is obtained through `/api/auth/me`.

---

## 6. Login

The initial screen is a minimal access terminal.

```text
BUSHIDO // CITADEL

SECURE TERMINAL ACCESS
────────────────────────────────

IDENTITY
> user@example.com

PASSPHRASE
> **************

[ AUTHENTICATE ]

NO IDENTITY // [ CREATE SPARTAN ]

────────────────────────────────
CITADEL NETWORK // DISCONNECTED
```

Login request:

```http
POST /api/auth/login
Content-Type: application/json
```

Body corresponds to `LoginRequest`:

```json
{
  "email": "user@example.com",
  "password": "..."
}
```

Successful response corresponds to `Token`:

```json
{
  "access_token": "..."
}
```

After receiving the token:

```text
POST /api/auth/login
        |
        v
receive JWT
        |
        v
GET /api/auth/me
Authorization: Bearer <JWT>
        |
        v
receive SpartanResponse
        |
        v
show terminal
```

---

## 7. Signup

Signup is available from the authentication screen.

Required fields:

```text
name
email
password
```

Request:

```http
POST /api/auth/signup
Content-Type: application/json
```

Example:

```json
{
  "name": "nj",
  "email": "user@example.com",
  "password": "..."
}
```

The signup endpoint already returns a `Token`.

Therefore:

```text
signup
  |
  v
receive JWT
  |
  v
GET /api/auth/me
  |
  v
authenticated terminal
```

The user does not need to manually login after successful signup.

---

## 8. Main terminal

Once authenticated:

```text
┌──────────────────────────────────────────────┐
│ BUSHIDO // CITADEL             ONLINE [●]   │
│ SPARTAN // nj                               │
├──────────────────────────────────────────────┤
│                                              │
│              OUTPUT HISTORY                  │
│                                              │
├──────────────────────────────────────────────┤
│ bushido>                                     │
└──────────────────────────────────────────────┘
```

A small logout action is available.

The command input receives focus whenever practical.

Enter submits the command.

---

## 9. Commands

Version 1 recognizes exactly two commands:

```text
log
load
```

The browser is not a shell.

There is:

- no arbitrary command execution
- no shell syntax
- no scripting
- no terminal emulator
- no ANSI interpreter

The terminal is simply the interaction model for the Bushido API.

---

## 10. `log`

Syntax:

```text
log <Citadel unit line>
```

Example:

```text
log squat 120 100 5
```

The frontend removes:

```text
log 
```

and sends the remaining line unchanged to Citadel.

Example:

```text
log squat 120 100 5
          |
          v
"squat 120 100 5"
```

Request:

```http
POST /api/unit/logs
Authorization: Bearer <token>
Content-Type: application/json
```

Body:

```json
{
  "line": "squat 120 100 5"
}
```

Citadel remains responsible for parsing the unit.

The frontend must not reimplement the Bushido unit grammar.

The authenticated Spartan is derived by Citadel from the bearer token.

The frontend must never send `spartan_id`.

Successful response:

```text
LoggedUnit
```

The returned structured unit is appended to terminal output.

---

## 11. `load`

`load` delegates filtering/query semantics to `LoadUnitRequest`.

The frontend constructs the appropriate `LoadUnitRequest` and calls:

```http
POST /api/unit/logs/query
Authorization: Bearer <token>
Content-Type: application/json
```

Response:

```text
list[LoggedUnit]
```

`LoggedUnit` remains structured.

The frontend must not convert loaded units into strings as part of the application model.

This is intentional because future versions may display:

- lifting sets
- running statistics
- HR values
- distances
- martial-arts sessions
- tables
- statistics
- charts

The initial terminal renderer may use a generic representation, but the underlying data remains structured.

---

## 12. `LoggedUnit`

`LoggedUnit` may represent multiple concrete unit variants.

The current API contract remains:

```python
list[LoggedUnit]
```

A particular query may enforce homogeneous results as a domain invariant even though Python's return annotation does not encode that invariant.

No generic/type-system redesign is required for v1.

Elm should model the API data according to the actual JSON representation returned by Citadel.

If necessary, a discriminated Elm union can later represent concrete unit types:

```elm
type LoggedUnit
    = Running RunningUnit
    | Lifting LiftingUnit
    | Cali CaliUnit
    | MartialArts MartialArtsUnit
    | ...
```

The exact decoder is determined by the real `LoggedUnit` JSON schema.

---

## 13. Terminal output

Terminal output contains entries such as:

```text
> log squat 120 100 5

[OK] UNIT LOGGED

...

> load squat

[OK] 14 RECORDS

...
```

Output entries should be represented as data rather than concatenating one giant terminal string.

Conceptually:

```elm
type TerminalEntry
    = CommandEntry String
    | InfoEntry String
    | ErrorEntry String
    | UnitEntry LoggedUnit
    | UnitListEntry (List LoggedUnit)
```

This allows richer rendering later without changing the command architecture.

---

## 14. Errors

Errors appear in the terminal/interface.

No browser `alert()`.

Examples:

```text
[ERROR 400]
Invalid lifting syntax
```

```text
[AUTH FAILED]
Invalid email or password
```

```text
[NETWORK ERROR]
Citadel unreachable
```

A 401 from an authenticated request invalidates the current session and returns the application to the authentication screen.

---

## 15. Unit names

Available unit names can be obtained through:

```http
GET /api/unit/names
```

Version 1 does not require autocomplete.

The endpoint may later support:

- autocomplete
- command hints
- validation assistance

Citadel remains the source of truth.

---

## 16. Background processing

Normal `log` and `load` operations remain synchronous.

```text
log
 |
 v
Citadel
 |
 +-- parse
 +-- validate
 +-- persist
 +-- commit
 |
 v
return LoggedUnit
```

When the frontend receives success, the operation has completed.

FastAPI `BackgroundTasks` are not used for core persistence.

Message queues may later be introduced for genuinely asynchronous secondary processing:

```text
log
 |
 v
Citadel
 |
 +----> PostgreSQL
 |        persist
 |
 +----> queue/event
           |
           +--> statistics
           +--> achievements
           +--> AI processing
           +--> external imports
```

Potential future Azure implementation:

```text
Citadel
   |
   v
Azure Storage Queue
   |
   v
worker / Container App Job
```

This is outside v1.

---

## 17. Elm model

Conceptually:

```elm
type alias Model =
    { auth : AuthState
    , token : Maybe String
    , command : String
    , output : List TerminalEntry
    , email : String
    , password : String
    , signupName : String
    , authMode : AuthMode
    }
```

Authentication mode:

```elm
type AuthMode
    = LoginMode
    | SignupMode
```

Authentication state:

```elm
type AuthState
    = LoggedOut
    | Authenticating
    | LoadingIdentity
    | LoggedIn Spartan
    | AuthFailed String
```

Messages correspond to application events rather than DOM implementation details.

---

## 18. Configuration

The API base URL exists in one place.

Development:

```text
http://localhost:8000
```

Production:

```text
https://api.bushido.nj-cyb.org
```

Endpoint URLs are derived from the base URL.

---

## 19. Security

The browser is untrusted.

Citadel performs all authorization.

The frontend must never decide whether a Spartan may access a unit.

Production passwords are sent only over HTTPS.

Never output:

- passwords
- password hashes
- bearer tokens
- Authorization headers
- database credentials

No Entra ID dependency is introduced.

---

## 20. Version 1 scope

Included:

```text
signup
login
/auth/me
logout
log
load
structured LoggedUnit responses
terminal history
error rendering
responsive layout
```

Excluded:

```text
dashboard
charts
statistics
editing
deleting
admin UI
password-reset email
OAuth
Entra ID
refresh-token system
WebSockets
message queues
background workers
autocomplete
command persistence
frontend routing
themes
complex animations
```

`/api/auth/change-password` exists but does not need a dedicated v1 screen.

---

## 21. Definition of done

```text
open frontend
      |
      v
login/signup
      |
      v
/auth/me
      |
      v
authenticated Spartan
      |
      v
terminal
      |
      +--> log <unit>
      |       |
      |       v
      |   /api/unit/logs
      |       |
      |       v
      |   LoggedUnit
      |
      +--> load ...
              |
              v
       /api/unit/logs/query
              |
              v
       list[LoggedUnit]
```

At this point Bushido is usable through the browser and further frontend work stops until after AZ-104.
