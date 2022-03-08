from importlib.abc import Loader
import util
import cv2
import yaml
from datetime import datetime
import concurrent.futures
import multiprocessing



path="Milestone1\Milestone1A.yaml"
with open(path) as f:
    data = yaml.load(f,Loader = yaml.SafeLoader)

def returnNestedDict(dict_obj):
    for key,value in dict_obj.items():
        if isinstance(value, dict):
            return returnNestedDict(value) 
        else:
            return dict_obj

def rec(dict_data,st):
    tasks = []
    for i in range(len(dict_data['Activities'])):
        tasks.append(list(dict_data['Activities'])[i])
        
    if dict_data['Type'] == 'Flow':
        if dict_data['Execution'] == 'Sequential':
            for i in range(len(tasks)):
                rec(dict_data['Activities'][tasks])
        else:            
            with concurrent.futures.ProcessPoolExecutor as p:
                p.map(rec,dict_data['Activities'][tasks])
    else:
        f = dict_data['Function']
        inp = [dict_data['Inputs']['FunctionInput'],int(dict_data['Inputs']['ExecutionTime'])]
        util.f(inp[0],inp[1])

st = ""
p = returnNestedDict(data)
rec(p,st)


