# Test Strategy: Restful-Booker API Automation

## 1. Scope and Target
- **Target Platform**: Restful-Booker (https://restful-booker.herokuapp.com)
- **Scope**: Authentication (`/auth`), Booking CRUD (`/booking`, `/booking/:id`), Query Filters, Health Check (`/ping`), and Persistence Verification.
- **Out of Scope**: Performance / load testing (explicitly forbidden on public shared sandbox), security penetration testing, contract testing.

## 2. Layered Architecture
Tests never call HTTP libraries directly. Logic is isolated into distinct layers:
1. **Configuration Layer** (`config/`): Pydantic-settings managing base URLs, credentials from environment (`.env`), and timeouts.
2. **Client Layer** (`src/clients/`): `BaseClient` wraps HTTP transport, retries, and latency logging. Specialised `AuthClient` and `BookingClient` expose domain actions.
3. **Data Factory Layer** (`src/factories/`): Dynamic Faker generators producing unique records with explicit overrides.
4. **Schema Layer** (`src/schemas/`): Pydantic models validating response contract conformity.
5. **Fixtures Layer** (`tests/conftest.py`): Session token management and self-cleaning `created_booking` fixtures.
6. **Test Layer** (`tests/`): Independent suites focused on CRUD, auth matrices, input boundaries, persistence, filtering, and end-to-end flows.

## 3. Resilience on a Public Shared Platform
Operating against a shared public sandbox requires specific mitigation strategies:
- **Automatic Cleanup**: Every created test resource is tracked and deleted during fixture teardown (`DELETE /booking/:id`).
- **Data Collision Isolation**: Faker generates unique UUID tags and names; assertions never inspect shared/seeded data.
- **Worker Throttle**: Parallel execution capped at `-n 2` to prevent hammering the shared host.
- **Targeted Connection Retries**: `HTTPTransport(retries=2)` handles transient TCP resets and cold starts without masking application-level errors.
- **Health Pre-Check**: CI runs a 5-step health loop before launching test suites.

## 4. Expected-Result Rule
- **Bug**: Documentation is explicit and implementation contradicts it (e.g. 500 on missing fields instead of 400).
- **Observation**: Documentation is silent and behavior is questionable (e.g. accepting negative prices or checkout before checkin). Documented as observations.
