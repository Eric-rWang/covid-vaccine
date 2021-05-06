# api.py

import json, pytz, datetime
from flask import Flask, request, send_file
import jobs

now_time = str(datetime.datetime.now(pytz.timezone('US/Central')))

app = Flask(__name__)

@app.route('/jobs', methods=['GET'])
def jobs_api():
#    try:
#        job = request.get_json(force=True)
#    except Exception as e:
#        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.return_jobs(), indent=2) + '\n'

@app.route('/load_data', methods=['GET'])
def load_data_api():
	return json.dumps(jobs.add_job('load_data', now_time), indent=2) + '\n'

@app.route('/create_data', methods=['POST'])
def create_data():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_data(data['location'], data['date'], data['fully_vaccinated']), indent=2) + '\n'

@app.route('/view_data', methods=['GET'])
def print_data():
    return json.dumps(jobs.get_view_data(), indent=2) + '\n'

@app.route('/update_data', methods=['POST'])
def change_data():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.update_data(data['location'], data['date'], data['fully_vaccinated']), indent=2) + '\n'

@app.route('/delete_data', methods=['POST'])
def remove_data():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.delete_data(data['date']), indent=2) + '\n'

@app.route('/graph_data', methods=['GET'])
def graph_data():
	return json.dumps(jobs.add_job('graph_data', now_time), indent=2) + '\n'

@app.route('/estimate', methods=['POST'])
def estimate_data():
    try:
        date = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job('estimate_vaccinated', now_time, date['date']), indent=2) + '\n'

@app.route('/view_result', methods=['POST'])
def view_result():
    try:
        jid = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.get_result(jid['jid']), indent=2) + '\n'

@app.route('/download/<jobid>', methods=['GET'])
def download(jobid):
    path = f'/app/{jobid}.png'
    with open(path, 'wb') as f:
        f.write(r3.hget(jobid, 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')








