from rq import Worker, Queue, Connection
from redis_conn import conn

if __name__ == "__main__":
  with Connection(conn):
    worker = Worker([Queue("default")])
    worker.work()

# runs forever and listens for new jobs to execute on the default queue
