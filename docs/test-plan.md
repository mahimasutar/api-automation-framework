# Test Plan: Restful-Booker API Automation

## Test Identifier Catalog

### Authentication Suite (`tests/auth/`)
| ID | Title | Target Endpoint | Expected Result | Type |
|---|---|---|---|---|
| AUTH-001 | Valid credentials login | `POST /auth` | 200 OK + token | Positive |
| AUTH-002 | Invalid password | `POST /auth` | 200 + Bad credentials | Negative |
| AUTH-003 | Unknown username | `POST /auth` | 200 + Bad credentials | Negative |
| AUTH-004 | Empty JSON body | `POST /auth` | 200 + Bad credentials | Negative |
| AUTH-005 | Missing password | `POST /auth` | 200 + Bad credentials | Negative |
| AUTH-006 | Missing username | `POST /auth` | 200 + Bad credentials | Negative |
| AUTH-007 | Basic auth header support | `PUT /booking/:id` | 200 OK | Positive |
| AUTH-008 | Bearer token rejected | `PUT /booking/:id` | 403 Forbidden | Negative |

### Auth Enforcement Matrix (`tests/auth/test_auth_enforcement.py`)
| ID | Title | Client | Method | Expected Status | State Invariant |
|---|---|---|---|---|---|
| AUTH-MAT-01 | Anon PUT | Anonymous | PUT | 403 Forbidden | Unchanged |
| AUTH-MAT-02 | Anon PATCH | Anonymous | PATCH | 403 Forbidden | Unchanged |
| AUTH-MAT-03 | Anon DELETE | Anonymous | DELETE | 403 Forbidden | Unchanged |
| AUTH-MAT-04 | Bad Token PUT | Invalid Token | PUT | 403 Forbidden | Unchanged |
| AUTH-MAT-05 | Bad Token PATCH | Invalid Token | PATCH | 403 Forbidden | Unchanged |
| AUTH-MAT-06 | Bad Token DELETE | Invalid Token | DELETE | 403 Forbidden | Unchanged |

### CRUD & Schema (`tests/crud/`)
| ID | Title | Target Endpoint | Expected Result | Type |
|---|---|---|---|---|
| CRUD-001 | Create booking success | `POST /booking` | 200 OK + bookingid | Positive |
| CRUD-002 | Get booking by ID | `GET /booking/:id` | 200 OK + full payload | Positive |
| CRUD-003 | PUT full update | `PUT /booking/:id` | 200 OK + updated data | Positive |
| CRUD-004 | PATCH partial update | `PATCH /booking/:id` | 200 OK + patched data | Positive |
| CRUD-005 | DELETE lifecycle | `DELETE /booking/:id` | 201 Created + 404 GET | Positive |
| CRUD-006 | Nonexistent ID | `GET /booking/:id` | 404 Not Found | Negative |
| CRUD-007 | Non-numeric ID | `GET /booking/:id` | 404 Not Found | Negative |
| CRUD-008 | Nonexistent DELETE | `DELETE /booking/:id` | 405 Method Not Allowed | Negative |
| CRUD-009 | PUT missing fields | `PUT /booking/:id` | 400 Bad Request | Negative |
| SCHEMA-001| Booking payload schema | `GET /booking/:id` | Pydantic conformant | Schema |
| SCHEMA-002| Booking response schema | `POST /booking` | Pydantic conformant | Schema |
| SCHEMA-003| List booking schema | `GET /booking` | List of integer IDs | Schema |

### Input Validation & Boundaries (`tests/validation/`)
| ID | Title | Target Scenario | Expected Status | Finding Status |
|---|---|---|---|---|
| VAL-001 | Missing firstname | `POST /booking` | 400 Bad Request | BUG-001 (returns 500) |
| VAL-002 | Missing lastname | `POST /booking` | 400 Bad Request | BUG-001 (returns 500) |
| VAL-003 | Missing totalprice | `POST /booking` | 400 Bad Request | BUG-001 (returns 500) |
| VAL-004 | Missing bookingdates | `POST /booking` | 400 Bad Request | BUG-001 (returns 500) |
| VAL-005 | String price type | `POST /booking` | 400 Bad Request | BUG-001 (returns 500) |
| VAL-006 | Zero price | `POST /booking` | 200 OK (< 500) | Handled |
| VAL-007 | Negative price | `POST /booking` | 200 OK (< 500) | Observation |
| VAL-008 | Large price | `POST /booking` | 200 OK (< 500) | Handled |
| VAL-009 | Inverted dates | `POST /booking` | 200 OK (< 500) | BUG-002 (no validation) |
| VAL-010 | Same-day dates | `POST /booking` | 200 OK (< 500) | Handled |
| VAL-011 | Malformed dates | `POST /booking` | < 500 | Handled |
| VAL-012 | Empty string name | `POST /booking` | < 500 | Handled |
| VAL-013 | Long string name | `POST /booking` | < 500 | Handled |
| VAL-014 | XSS / Special chars | `POST /booking` | < 500 | Sanitized/Stored |

### Persistence & Filters (`tests/persistence/`, `tests/filters/`, `tests/e2e_flows/`)
| ID | Title | Scope | Expected Result |
|---|---|---|---|
| PERSIST-001 | Create + GET roundtrip | Persistence | All fields match payload |
| PERSIST-002 | PUT roundtrip | Persistence | New fields saved, ID stable |
| PERSIST-003 | PATCH roundtrip | Persistence | Target updated, others unchanged |
| PERSIST-004 | List index presence | Persistence | ID in `/booking` list |
| PERSIST-005 | Delete index purging | Persistence | Purged from GET and list |
| PERSIST-006 | Failed create isolation | Persistence | No phantom IDs added |
| FILTER-001 | Filter by firstname | Filters | Matches created ID |
| FILTER-002 | Filter by lastname | Filters | Matches created ID |
| FILTER-003 | Filter by combo names | Filters | Matches created ID |
| FILTER-004 | Filter checkin date | Filters | Matches created ID |
| FILTER-005 | Filter checkout date | Filters | Matches created ID |
| FILTER-006 | Filter nonexistent | Filters | Returns `[]` |
| E2E-001 | Full guest lifecycle | E2E | Create -> Read -> PUT -> PATCH -> Filter -> DELETE |
| E2E-002 | Multi-booking isolation | E2E | Queries isolate separate bookings |
