import threading
import pandas as pd
from datetime import datetime
import yaml
import sys
import util

class Logger:
    
    data = {}
    cur = ''
    concur = False
    threadLock = threading.Lock()
    def __init__(self,data,cur = '',concurrent = False):
        global time
        self.data = data
        self.cur = cur
        self.concur = concurrent
        threads = []
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.cur+' Entry')
        self.threadLock.release()
        k = data['Activities']
        
        for j in k:
            if k[j]['Type'] =='Task':
                if self.concur:
                    t_temp = threading.Thread(target = self.exec_func,args=(j,k))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    self.exec_func(j,k)
            else:
                #print(k[j])
                l = k[j]['Execution'] == 'Concurrent'
                if self.concur:
                    t_temp = threading.Thread(target=Logger, args = (k[j],self.cur+'.'+j,l))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    Logger(data = k[j],cur = self.cur+'.'+j,concurrent = l)
                    #del next
        for x in threads:
            x.join()

    def __del__(self):
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.cur+' Exit')
        self.threadLock.release()


    def conditions(self,con):
        global ops
        var = ''
        st = 0
        ed = 0
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

    def exec_func(self,name,k):
        global path,ops
        func = k[name]['Function']
        inputs = k[name]['Inputs']
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.cur+'.'+name+' Entry')
        self.threadLock.release()

        if 'Condition' in k[name]:
            if not self.conditions(k[name]['Condition']):
                self.threadLock.acquire()
                print(str(datetime.now())+';'+self.cur+'.'+name+' Skipped' )
                self.threadLock.release()

                self.threadLock.acquire()
                print(str(datetime.now())+';'+self.cur+'.'+name+' Exit')
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
            print(str(datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ('+str(f_input)+' , '+inputs['ExecutionTime']+')' )
            self.threadLock.release()

            util.TimeFunction(inputs['ExecutionTime'])

        if func == "DataLoad":
            self.threadLock.acquire()
            print(str(datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ('+inputs['Filename']+')' )
            self.threadLock.release()
            
            temp = util.DataLoad(path+'/'+inputs['Filename'])
            ops[self.cur+'.'+name+'.NoOfDefects'] = temp['NoOfDefects']
            
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.cur+'.'+name+' Exit')
        self.threadLock.release()


dts = {}
ops = {}
path = "Milestone1"

with open('Milestone1\Milestone1A.yaml','r') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

orig_stdout = sys.stdout
f = open('M1A_output.txt', 'w')
sys.stdout = f

for i in data:
    if data[i]['Execution'] =='Sequential':
        p1 = Logger(data[i],i)
        del p1

sys.stdout = orig_stdout
f.close()