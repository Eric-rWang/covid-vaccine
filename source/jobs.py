# jobs.py

import uuid, json, redis, os, csv

from hotqueue import HotQueue

q = HotQueue("queue", host='10.99.12.229', port=6379, db=1)
rd = redis.StrictRedis(host='10.99.12.229', port=6379, db=0)
r2 = redis.StrictRedis(host='10.99.12.229', port=6379, db=2)
#worker_ip = os.environ.get('WORKER_IP')

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, time, status, task, pod_ip="not_set"):
    if type(jid) == str:
        return {'id': jid,
                'time': time,
                'status': status,
                'task': task,
                'pod_ip': pod_ip
        }
    return {'id': jid.decode('utf-8'),
            'time': time.decode('utf-8'),
            'status': status.decode('utf-8'),
            'task': task.decode('utf-8'),
            'pod_ip': pod_ip
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(task, time, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, time, status, task)
    # update call to save_job:
    _save_job(_generate_job_key(jid), job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict

def update_job_status(jid, worker_ip, new_status):
    """Update the status of job with job id `jid` to status `status`."""
    jid, time, status, task = rd.hmget(_generate_job_key(jid), 'id', 'time', 'status', 'task')
    print(task, type(task))

    if new_status == "in progress":
        print('test2')
        if task == b'jobs':
            return_jobs()
        elif task == b'load_data':
            print('test3')
            load_data()

    print('test4')

    job = _instantiate_job(jid, time, status, task, worker_ip)
    if job:
        job['status'] = new_status
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()

def return_jobs():
    keys = rd.keys()
    jobs = []
    for key in keys:
        key = key.decode("utf-8")
        jobs.append(rd.hgetall(key))

    return jobs

def load_data():
    print('load_data')
    with open('us_vaccine_data.csv', 'r') as csv_in:
        csv_file = csv.reader(csv_in, delimiter=',')
        data = {"vaccine_data":[]}
        header = next(csv_file, None)
        
        for line in csv_file:
            data['vaccine_data'].append({
                'location': str(line[0]),
                'date': str(line[1]),
                'vaccinated': int(line[2])
            })
        
        r2.set('vaccine_data', json.dumps(data, indent = 2))

















