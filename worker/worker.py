import redis
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


# while True:
#     job = r.brpop("job", timeout=5)
#     if job:
#         _, job_id = job
#         process_job(job_id.decode())
while True:
    # 4. CRITICAL FIX: Changed "job" to "jobs" (plural) to match api/main.py
    # If these don't match, your integration tests will FAIL.
    job = r.brpop("jobs", timeout=5)
    if job:
        # job is a tuple: (list_name, job_id)
        _, job_id = job
        process_job(job_id)
