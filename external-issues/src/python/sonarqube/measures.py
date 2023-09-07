#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import json
import requests
import sonarqube.env
import sonarqube.sqobject

class Measure (sonarqube.sqobject.SqObject):

    def __init__(self, name = None, value = None, **kwargs):
        self.name = name
        self.value = value
        self.history = None
        self.env = kwargs['env']

    def read(self, project_key, metric_key):
        parms = dict(component=project_key, metricKeys=metric_key)
        resp = self.get('/api/measures/component',  parms)
        data = json.loads(resp.text)
        return data['component']['measures']

    def get_history(self, project_key):
        parms = dict(component=project_key, metrics=self.name, ps=1000)
        resp = self.get('/api/measures/search_history',  parms)
        data = json.loads(resp.text)
        return data['component']['measures']

def load_measures(project_key, metrics_list, myenv = None):
    parms = dict(component=project_key, metricKeys=metrics_list)
    if (myenv is None):
        resp = sonarqube.env.get('/api/measures/component',  parms)
    else:
        resp = myenv.get('/api/measures/component', parms)
    data = json.loads(resp.text)
    return data['component']['measures']

