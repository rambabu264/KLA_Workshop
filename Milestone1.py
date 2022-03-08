from importlib.abc import Loader
from util import *
import cv2
import yaml
from datetime import datetime
import concurrent.futures
import multiprocessing



path="Milestone1\Milestone1A.yaml"
with open(path) as f:
    data = yaml.load(f,Loader = yaml.SafeLoader)

def func(dict_obj):
    for key,value in dict_obj.items():
        if isinstance(value,dict):
            for pair in func(value) :
                yield(key,*pair)
        else:
            yield(key,value)

log = set()
st = ""

def reading_file(pair,st):
    st += str(datetime.now())+";"+str(pair[0])
    if pair[1] == 'Type':
        log.add(st+" Entry")
        if pair[2] == 'Sequential':
            pass
        elif pair[2] == 'Concurrent':
            with concurrent.futures.ProcessPoolExecutor as p:
                f = p.submit()


'''
    st = 
    solve(pair)

    print(st)

create_csv("log",log)
'''
x = func(data)
p = x.__next__()
print(p[0:1])
'''
flow = ""
Execution = ""


while p:
    #reading_file(p)
    if len(p) == 3:
        st = str(datetime.now())+";"+str(p[0])
        log.add(st)
        if p[2] == 'Flow':
        flow = "Flow"
    else:
        
    p = x.__next__()

'''