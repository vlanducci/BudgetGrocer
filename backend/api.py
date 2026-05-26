from fastapi import FastAPI
from pydantic import BaseModel
from rq import Queue
from redis_conn import conn
from jobs import scrape_job

app = FastAPI()
q = Queue(connection=conn)

class RequestBody(BaseModel):
  query: str

@app.post("/enqueue")
def enqueue(body: RequestBody):
  job = q.enqueue(scrape_job, body.query)
  return {"job_id": job.id}