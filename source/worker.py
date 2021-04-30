# worker.py
import time, os
from jobs import q, update_job_status

worker_ip = os.environ.get('WORKER_IP')

@q.worker
def execute_job(jid):
    update_job_status(jid, worker_ip, "in progress")
    time.sleep(15)
    update_job_status(jid, worker_ip, "complete")

execute_job()