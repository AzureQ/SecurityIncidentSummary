## SecurityIncidentSummary

### Pre-requisite

`conda` - The project uses conda as environemnt manager, please install conda or anaconda(even better)

### Environment Preparation 

Clone the repo, then run below commands:
```
cd SecurityIncidentSummary
conda env create --file environment.yaml
conda activate SecurityIncidentSummary
```

Check if the conda environment - `SecurityIncidentSummary` is created successfully

`conda env list`

### Run the App

```
cd SecurityIncidentSummary
export ELEVATE_USERNAME=<username of the endpoint> 
export ELEVATE_PASSWORD=<password of the endpoint>
export FLASK_APP=src/app.py 
export FLASK_RUN_PORT=9000
python -m flask run
```

Then go to http://localhost:9000/incidents to check the aggregated incidents

### Unittest

`
cd SecurityIncidentSummary
python -m unittest tests/test_data_processing.py
`
