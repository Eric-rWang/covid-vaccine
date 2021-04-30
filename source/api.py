# api.py

import json, pytz, datetime
from flask import Flask, request
import jobs

now_time = str(datetime.datetime.now(pytz.timezone('US/Central')))

app = Flask(__name__)

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job('jobs', now_time))

@app.route('/load_data', methods=['GET'])
def load_data_api():
	return json.dumps(jobs.add_job('load_data', now_time))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')