from fastapi import FastAPI
import redis
import uuid
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your React URL
    allow_methods=["*"],
    allow_headers=["*"],
)



# r = redis.Redis(host="localhost", port=6379)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

#jobs endpoint
@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}


# single job status endpoint
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status.decode()}


@app.get("/health")
def health_check():
    try:
        r.ping() # Check if Redis is reachable
        return {"status": "healthy"}
    except Exception:
        return {"status": "unhealthy"}, 500
