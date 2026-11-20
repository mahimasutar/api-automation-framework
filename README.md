# Restful-Booker API Automation Framework

![CI Status](https://github.com/tanma/API_automation_framework/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)
![Pytest](https://img.shields.io/badge/tested%20with-pytest-yellow.svg)
![Allure](https://img.shields.io/badge/reporting-allure-orange.svg)

Production-grade, layered API test automation framework for the public **Restful-Booker** testing platform. Built with Python, pytest, httpx, Faker, Pydantic, and Allure, orchestrated via GitHub Actions CI.

---

## Architecture Overview

```
API_automation_framework/
├── .github/workflows/ci.yml     # Automated CI pipeline with health checks & parallel jobs
├── config/
│   ├── settings.py              # Pydantic BaseSettings loaded from config/.env
│   ├── .env.example             # Committed credential template
│   └── .env                     # Local credentials (ignored)
├── src/
│   ├── clients/                 # Layered API HTTP clients
│   │   ├── base_client.py       # Httpx client wrapper (logging, retries, latency)
│   │   ├── auth_client.py       # POST /auth endpoints
│   │   └── booking_client.py    # CRUD, ping, and filter endpoints
│   ├── factories/               # Dynamic data generation
│   │   └── booking_factory.py   # Faker-backed payload generator with overrides
│   ├── schemas/                 # Pydantic contract validation
│   │   └── booking_schema.py    # Request & response schema definitions
│   └── utils/
├── tests/
│   ├── conftest.py              # Session auth token & self-cleaning fixtures
│   ├── smoke/                   # Fast critical availability checks (ping, token)
│   ├── auth/                    # Token generation & access control matrix
│   ├── crud/                    # Full CRUD operations & schema conformity
│   ├── validation/              # Equivalence partitioning & input boundaries
│   ├── persistence/             # Round-trip read-back verification
│   ├── filters/                 # Query parameter search tests
│   └── e2e_flows/               # End-to-end multi-step guest lifecycles
├── docs/
│   ├── test-strategy.md         # Architecture, design principles, risk mitigation
│   ├── test-plan.md             # Traceability catalog (AUTH-001 to E2E-002)
│   └── bug-reports/             # Real reproducible defects (BUG-001 to BUG-003)
├── pytest.ini                   # Markers, reruns, logging, allure configuration
└── requirements.txt             # Dependency specification
```

---

## Test Suites and Coverage Breakdown

| Suite | Focus Area | Marker | Total Tests |
|---|---|---|:---:|
| **Smoke** | Platform health check and critical auth | `smoke` | 5 |
| **Auth** | Positive/negative token generation & auth headers | `auth` | 8 |
| **Auth Matrix** | Parameterized access control (PUT/PATCH/DELETE) | `auth` | 6 |
| **CRUD** | Resource create, read, update, delete | `crud` | 9 |
| **Schema** | Pydantic strict response contract validation | `schema` | 3 |
| **Validation** | Boundary values, negative types, string limits | `validation` | 14 |
| **Persistence** | Secondary read verification & state invariants | `persistence` | 6 |
| **Filters** | Query parameter search (names, dates, combos) | `filters` | 6 |
| **E2E Flows** | Multi-step guest lifecycle and record isolation | `e2e` | 2 |
| **Total** | | | **57** |

---

## Engineering Highlights & Resilience Patterns

1. **Shared Environment Isolation**:
   - Every test creates isolated test data using Faker and unique UUID tags. Tests never depend on seeded data that resets every 10 minutes.
   - Self-cleaning `created_booking` fixture guarantees teardown deletion via HTTP `DELETE`.
2. **Persistence Round-Trips**:
   - Because public testing sandboxes grant no direct database access, all persistence assertions are verified via secondary read round-trips (`GET /booking/:id` and list indexing).
3. **Throttled Parallel Execution**:
   - Test suites execute with `pytest -n 2`. Tests are strictly isolated and pass independently in parallel without state collisions.
4. **Resilience & Cold Starts**:
   - `HTTPTransport(retries=2)` handles transport-level connection errors.
   - `pytest-rerunfailures` automatically retries flaky network drops (`--reruns 1 --reruns-delay 2`).
5. **CI Health Pre-Check**:
   - GitHub Actions workflow checks `/ping` in a 5-step retry loop prior to suite execution to avoid false negatives when target is sleeping.

---

## Real Bug Reports Discovered
Real defects discovered against the live target are catalogued in [`docs/bug-reports/`](file:///c:/Users/tanma/Mahima/API_automation_framework/docs/bug-reports/):
- **[BUG-001](file:///c:/Users/tanma/Mahima/API_automation_framework/docs/bug-reports/BUG-001.md)**: `POST /booking` returns unhandled `500 Internal Server Error` instead of `400 Bad Request` on missing payload properties.
- **[BUG-002](file:///c:/Users/tanma/Mahima/API_automation_framework/docs/bug-reports/BUG-002.md)**: `POST /booking` allows checkout date earlier than checkin date (`checkout < checkin`).
- **[BUG-003](file:///c:/Users/tanma/Mahima/API_automation_framework/docs/bug-reports/BUG-003.md)**: `DELETE /booking/:id` returns `201 Created` instead of `200/204`.

---

## Quickstart

### 1. Setup Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `config/.env` and update credentials if needed:
```bash
cp config/.env.example config/.env
```

### 3. Run Tests
- **Fast Smoke Tests**:
  ```bash
  pytest -m smoke
  ```
- **Full Regression Suite (Parallel)**:
  ```bash
  pytest -m regression -n 2
  ```
- **Specific Feature Suite**:
  ```bash
  pytest tests/auth/ -v
  pytest tests/persistence/ -v
  ```

### 4. Generate Allure Report
```bash
allure serve allure-results
```
