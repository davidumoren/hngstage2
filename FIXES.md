# FIXES.md — Bug Report

## Bug 1: `api/main.py` line 8 — Hardcoded Redis host
**File:** `api/main.py`  
**Line:** 8  
**Problem:** `redis.Redis(host="localhost", ...)` — localhost doesn't resolve inside a Docker container to another container.  
**Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")` so the host is configurable via environment variable.

## Bug 2: `api/main.py` line 8 — Redis password not configured
**File:** `api/main.py`  
**Line:** 8  
**Problem:** Redis connection had no password support, but `.env` defined `REDIS_PASSWORD`.  
**Fix:** Added `password=os.getenv("REDIS_PASSWORD", None)` to the Redis connection.

## Bug 3: `api/main.py` line 12 — Wrong Redis queue key name
**File:** `api/main.py`  
**Line:** 12  
**Problem:** `r.lpush("job", job_id)` uses key `"job"` but `worker.py` reads from `"job"` via `brpop("job", ...)` — inconsistent. Standardized both to `"jobs"` (plural) for clarity, and both files now use `"jobs"`.  
**Fix:** Changed `r.lpush("job", ...)` to `r.lpush("jobs", ...)` in API; changed `r.brpop("job", ...)` to `r.brpop("jobs", ...)` in worker.

## Bug 4: `worker/worker.py` line 6 — Hardcoded Redis host
**File:** `worker/worker.py`  
**Line:** 6  
**Problem:** `redis.Redis(host="localhost", ...)` — same container networking issue.  
**Fix:** Changed to use `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` from environment variables.

## Bug 5: `worker/worker.py` line 7 — Unused import
**File:** `worker/worker.py`  
**Line:** 4  
**Problem:** `import signal` was imported but never used — flake8 violation.  
**Fix:** Removed the unused import.

## Bug 6: `frontend/app.js` line 6 — Hardcoded API URL
**File:** `frontend/app.js`  
**Line:** 6  
**Problem:** `const API_URL = "http://localhost:8000"` — localhost doesn't route to the API container.  
**Fix:** Changed to `const API_URL = process.env.API_URL || 'http://api:8000'`.

## Bug 7: `api/.env` committed to repository
**File:** `api/.env`  
**Problem:** A `.env` file containing `REDIS_PASSWORD=supersecretpassword123` was committed. This is a critical security issue.  
**Fix:** Deleted `api/.env`, added `.env` and `**/.env` to `.gitignore`, and created `.env.example` with placeholder values.

## Bug 8: No `/health` endpoint in API
**File:** `api/main.py`  
**Problem:** No health endpoint existed, making Docker HEALTHCHECK and `depends_on: condition: service_healthy` impossible.  
**Fix:** Added `GET /health` endpoint that pings Redis and returns `{"status": "ok"}` or 503.

## Bug 9: No `/health` endpoint in frontend
**File:** `frontend/app.js`  
**Problem:** Same as above — no health endpoint for Docker to poll.  
**Fix:** Added `GET /health` that returns `{"status": "ok"}`.

## Bug 10: No `.gitignore`
**Problem:** No `.gitignore` existed, risking `.env` files, `node_modules`, and `__pycache__` being committed.  
**Fix:** Added `.gitignore` with appropriate entries.