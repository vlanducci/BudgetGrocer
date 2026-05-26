from rq import Worker, Queue
from redis_conn import conn

if __name__ == "__main__":
    queue = Queue("default", connection=conn)
    worker = Worker([queue], connection=conn)
    worker.work()

# runs forever and listens for new jobs to execute on the default queue
