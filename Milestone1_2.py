import threading
import pandas as pd
from datetime import datetime
import yaml
import sys
import util

class Workflow:
    
    data = {}
    current = ''
    concur = False
    threadLock = threading.Lock()
    def __init__(self,data,cur = '',concurrent = False):
        global time
        self.data = data
        self.current = cur
        self.concur = concurrent
        threads = []
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.current+' Entry')
        self.threadLock.release()
        act = data['Activities']
        
        for j in act:
            if act[j]['Type'] =='Task':
                if self.concur:
                    t_temp = threading.Thread(target = self.exec_func,args=(j,act))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    self.exec_func(j,act)
            else:
                #print(k[j])
                l = act[j]['Execution'] == 'Concurrent'
                if self.concur:
                    t_temp = threading.Thread(target=Workflow, args = (act[j],self.current+'.'+j,l))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    Workflow(data = act[j],cur = self.current+'.'+j,concurrent = l)
                    #del next
        for x in threads:
            x.join()


    def exec_func(self,name,act):
        global path,ops

        func = act[name]['Function']
        inputs = act[name]['Inputs']
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.current+'.'+name+' Entry')
        self.threadLock.release()
            
        if 'Condition' in act[name]:
            if not self.conditions(act[name]['Condition']):
                self.threadLock.acquire()
                print(str(datetime.now())+';'+self.current+'.'+name+' Skipped' )
                self.threadLock.release()

                self.threadLock.acquire()
                print(str(datetime.now())+';'+self.current+'.'+name+' Exit')
                self.threadLock.release()

                return
            
        if func == "TimeFunction":
            f_input = inputs['FunctionInput']
            if '$' in inputs['FunctionInput']:
                st = 0
                ed = 0
                for i in range(len(f_input)):
                    if f_input[i] == '(':
                        st = i
                    if f_input[i] == ')':
                        ed = i
                f_input = ops[f_input[st+1:ed]]
            self.threadLock.acquire()
            print(str(datetime.now())+';'+self.current+'.'+name+' Executing '+func+' ('+str(f_input)+' , '+inputs['ExecutionTime']+')' )
            self.threadLock.release()

            util.TimeFunction(inputs['ExecutionTime'])

        if func == "DataLoad":
            self.threadLock.acquire()
            print(str(datetime.now())+';'+self.current+'.'+name+' Executing '+func+' ('+inputs['Filename']+')' )
            self.threadLock.release()
            
            temp = util.DataLoad(path+'/'+inputs['Filename'])
            ops[self.current+'.'+name+'.NoOfDefects'] = temp['NoOfDefects']
            
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.current+'.'+name+' Exit')
        self.threadLock.release()

    def conditions(self,con):
        global ops
        var = ''
        st,ed = (0,0)
        gr = True
        f = 0
        for i in range(len(con)):
            if con[i] == '(':
                st = i
            if con[i] == ')':
                ed = i
            if con[i] == '<':
                gr = False
                f = i+1
            if con[i] == '>':
                f = i+1
        var = con[st+1:ed]
        n = int(con[f+1:])
        while var not in ops:
            h = 0
        if gr:
            if ops[var]> n:
                return True
        else:
            if ops[var]< n:
                return True

        return False

                
    def Finish(self):
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.current+' Exit')
        self.threadLock.release()


dts = {}
ops = {}
path = "Milestone2"

with open('Milestone2\Milestone2A.yaml','r') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

fout = sys.stdout
f = open('M2A_output.txt', 'w')
sys.stdout = f

for i in data:
    if data[i]['Execution'] =='Sequential':
        p1 = Workflow(data[i],i)
        p1.Finish()


sys.stdout = fout
f.close()