# jobs.py

import uuid, json, redis, os, csv, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from numpy import arange
from scipy.optimize import curve_fit
from datetime import date
from hotqueue import HotQueue

q = HotQueue("queue", host='10.99.12.229', port=6379, db=1)
rd = redis.StrictRedis(host='10.99.12.229', port=6379, db=0)
r2 = redis.StrictRedis(host='10.99.12.229', port=6379, db=2)
r3 = redis.StrictRedis(host='10.99.12.229', port=6379, db=3)
#worker_ip = os.environ.get('WORKER_IP')

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, time, status, task, job_input, pod_ip="not_set"):
    if type(jid) == str:
        return {'id': jid,
                'time': time,
                'status': status,
                'task': task,
                'job_input': job_input,
                'pod_ip': pod_ip
        }
    return {'id': jid.decode('utf-8'),
            'time': time.decode('utf-8'),
            'status': status.decode('utf-8'),
            'task': task.decode('utf-8'),
            'job_input': job_input,
            'pod_ip': pod_ip
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(task, time, job_input="none", status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, time, status, task, job_input)
    # update call to save_job:
    _save_job(_generate_job_key(jid), job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict

def update_job_status(jid, worker_ip, new_status):
    """Update the status of job with job id `jid` to status `status`."""
    jid, time, status, task, job_input = rd.hmget(_generate_job_key(jid), 'id', 'time', 'status', 'task', 'job_input')

    if new_status == "in progress":
        if task == b'load_data':
            load_data()
        elif task == b'graph_data':
            graph_data(jid)
        elif task == b'estimate_vaccinated':
            print(type(job_input))
            job_input = job_input.decode('utf-8')
            print(type(job_input))
            estimate_vaccinated(jid, job_input)

    job = _instantiate_job(jid, time, status, task, job_input, worker_ip)
    if job:
        job['status'] = new_status
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()

def return_jobs():
    keys = rd.keys()
    jobs = {"jobs":[]}

    for key in keys:
        key = key.decode("utf-8")
        jid, time, status, task, job_input, pod_ip = rd.hmget(key, 'id', 'time', 'status', 'task', 'job_input', 'pod_ip')

        jobs["jobs"].append({
            'id': jid.decode('utf-8'),
            'time': time.decode('utf-8'),
            'status': status.decode('utf-8'),
            'task': task.decode('utf-8'),
            'job_input': job_input.decode('utf-8'),
            'pod_ip': pod_ip.decode('utf-8')
        })

    return jobs

def load_data():
    with open('us_vaccine_data.csv', 'r') as csv_in:
        csv_file = csv.reader(csv_in, delimiter=',')
        data = {"vaccine_data":[]}
        header = next(csv_file, None)
        
        for line in csv_file:
            data['vaccine_data'].append({
                'location': str(line[0]),
                'date': str(line[1]),
                'vaccinated': float(line[2])
            })
        
        r2.set('vaccine_data', json.dumps(data, indent = 2))

# Graph the data, save it under r3 with it's jid as the key.
def graph_data(jid):
    dates, fully_vaccinated = get_data()

    x_values = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in dates]

    plt.plot(x_values, fully_vaccinated)
    plt.xlabel("Date")
    plt.ylabel("Fully Vaccinated")
    plt.title("Number of Fully Vaccinated People in the US")
    plt.ylim(1342086.0, 96747454.0)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    #plt.savefig('vaccinated_graph.png')
    plt.show()

# Given a date, estimate the total vaccinated people 
def estimate_vaccinated(jid, date_input):

    if date_input != b'none':
        dates, fully_vaccinated = get_data()
        x = list(range(len(dates)))

        popt, _ = curve_fit(objective, x, fully_vaccinated)
        a, b, c, d = popt
        #print('y = %.5f * x^3 + %.5f * x^2 + %.5f * x + %.5f' % (a, b, c, d))

        '''
        plt.scatter(x,fully_vaccinated, s=1)
        plt.xlabel("Date")
        plt.ylabel("Fully Vaccinated")
        plt.title("Number of Fully Vaccinated People in the US")
        x_line = arange(min(x), max(x), 1)
        y_line = objective(x_line, a, b, c, d)
        plt.plot(x_line, y_line, '--', color='green')
        plt.show()
        '''

        date1 = dates[0].split('-')
        date2 = date_input.split('-')

        f_date = date(int(date1[0]), int(date1[1]), int(date1[2]))
        l_date = date(int(date2[0]), int(date2[1]), int(date2[2]))
        delta = l_date - f_date
        #print(delta.days)

        est_vaccinted = round(objective(delta.days, a, b, c, d))
        return_data = {"result":[]}

        return_data['result'].append({
                'jid': str(jid),
                'location': 'United States',
                'date': str(date_input),
                'fully vaccinated estimate': str(est_vaccinted)
        })

        r3.set(jid, json.dumps(return_data, indent = 2))

    else:
        population_us = 328200000

        # calculate herd immunity


def objective(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def get_data():
    clean_data = json.loads(r2.get('vaccine_data').decode('utf-8'))
    dates = []
    fully_vaccinated = []

    for i in range(len(clean_data['vaccine_data'])):
        dates.append(clean_data['vaccine_data'][i]['date'])
        fully_vaccinated.append(clean_data['vaccine_data'][i]['vaccinated'])

    return dates, fully_vaccinated

def get_result(jid):
    job_id = _generate_job_key(jid)

    data = {"result":[]}

    try: 
        return json.loads(r3.get(jid))
    except Exception as e:
        return "Unable to find job: " + str(jid)

def get_view_data():
    return json.loads(r2.get('vaccine_data'))






