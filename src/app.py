from flask import Flask
import asyncio
import time
from src import data_processing
from src.data_intake import fetch_incidents_async

app = Flask(__name__)
app.config.from_object('config.Config')


@app.route('/incidents')
def hello_incidents():
    incident_types = app.config['ELEVATE_INCIDENT_TYPES']
    base_url = app.config['ELEVATE_BASE_URL']

    start_time = time.time()

    # fetch all types of incidents from different endpoint
    # url looks like: https://incident-api.use1stag.elevatesecurity.io/incidents/<type>
    # ref doc: https://gist.github.com/amissemer/8314efe851f979670f026c10161267f6#incident-source-endpoints
    incident_lists = asyncio.run(fetch_incidents_async(base_url=base_url + '/incidents', incident_types=incident_types))

    # fetch identities mapping in format of [{<ip>:<employee_id>, ...}]
    identities_lists = asyncio.run(fetch_incidents_async(base_url=base_url, incident_types=['identities']))

    # preprocess json response lists
    processed = data_processing.pre_process(incident_lists, incident_types, identities_lists)

    # load all preprocessed into dataframe
    # aggregate data by employee_id, priority
    # sort grouped incidents in ascending order
    df_result = data_processing.aggregate_by_emp_priority(processed)
    print("Process took %s seconds" % (time.time() - start_time))

    return df_result.to_json(orient='index', indent=2)


if __name__ == '__main__':
    app.run(port='9000')
