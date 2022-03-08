from importlib.abc import Loader
#from util import *
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
p = returnNestedDict(data)
#rec(p)
k = list(p['Activities'])[0]
print(p['Activities'][k])


def rec(dict_data):
    tasks = []
    for i in len(dict_data['Activities']):
        tasks.append(list(dict_data['Activities'])[i])
        
    if dict_data['Type'] == 'Flow':
        if dict_data['Execution'] == 'Sequential':
            for i in len(tasks):
                rec(p['Activities'][tasks])
        else:            
            with concurrent.futures.ProcessPoolExecutor as p:
                p.map(rec,p['Activities'][tasks])
    else:
                

'''
def iter_dict(dict_obj):
    for key,value in dict_obj.items():
        if isinstance(value,dict):
            for pair in iter_dict(value) :
                yield(key,*pair)
        else:
            yield(key,value)

log = set()
st = ""

def reading_file(pair,st):
    if pair[1] == 'Type':
        log.add(st+" Entry")
    elif pair[1] == 'Flow':
        pair = x.__next__()
        reading_file(pair[])



    st = 
    solve(pair)

    print(st)

create_csv("log",log)

x = func(data)
p = x.__next__()

flow = ""
Execution = ""


while p:
    if len(p) == 3:
        st = str(datetime.now())+";"+str(p[0])
        log.add(st)
        p = x.__next__()
    reading_file(p[1:],st)        
    p = x.__next__()
'''
