from fastapi import FastAPI
from pydantic import BaseModel
from rq import Queue
from redis_conn import conn
from jobs import scrape_job, get_results
from rq.job import Job


app = FastAPI()
q = Queue(connection=conn)

class RequestBody(BaseModel):
  query: str

@app.post("/enqueue")
def enqueue(body: RequestBody):
  job = q.enqueue(scrape_job, body.query)
  return {"job_id": job.id}


@app.get("/results/{job_id}")
def results(job_id: str):
    job = Job.fetch(job_id, connection=conn)

    if job.is_finished:
        return {
            "status": "finished",
            "results": job.result
        }

    if job.is_failed:
        return {
            "status": "failed",
            "error": str(job.exc_info)
        }

    return {
        "status": "running",
        "results": None
    }