'''
import yaml
import pandas as pd
import threading as td
from datetime import datetime 
from util import *

#function to create a log line
def log_file(str_template):
    string = str(datetime.now()) + ';'
    for x in range(len(str_template)):
        string += str_template[x]
        if x < (len(str_template) - 1):
            string += '.'
    return string


#here the activities are parsed
def exec(activity, str_template, txt_lines):
    
    #parsing the activities to execute them
    list_tasks = list(activity.keys())
    for x in list_tasks:
        task = activity[x]
        str_template.append(x)
        line = log_file(str_template) + " Entry\n"
        txt_lines.append(line)
        task_attr = list(task.keys())
        # change to required conditional expression
        condition = 1
        if "Execution" in task_attr:
            sub_flow = task['Activities']
            exec(sub_flow, str_template, txt_lines)
        else:
            if task['Function'] == 'TimeFunction' and condition:
                op_str = log_file(str_template)
                task_input = task['Inputs']
                exec_time = int(task_input['ExecutionTime'])
                op_str += " Executing TimeFunction("
                op_str += task_input['FunctionInput'] + ","
                op_str += str(exec_time) + ")\n"
                txt_lines.append(op_str)
                TimeFunction(exec_time)
        line = log_file(str_template) + " Exit\n"
        txt_lines.append(line)
        str_template.pop(-1)
    
if __name__ == "__main__":
    path="Milestone1\Milestone1B.yaml"
    with open(path) as ip_file:
            ip_data = yaml.load(ip_file, Loader=yaml.FullLoader)
            log_file = open("Output\Milestone1B.txt", "a+")
            workflow_keys = list(ip_data.keys())
            for x in workflow_keys:
                txt_lines = []
                str_template = [x]
                task_string = log_file(str_template) + " Entry\n"
                txt_lines.append(task_string)
                workflow = ip_data['M1B_Workflow']
                activity = workflow['Activities']
                exec(activity, str_template, txt_lines)
                task_string = log_file(str_template) + " Exit\n"
                txt_lines.append(task_string)
                log_file.writelines(txt_lines)
                print("Workflow {} has been logged".format(x))
            print("File Created!")
            log_file.close()
'''
import yaml
with open('Milestone1\Milestone1A.yaml','r') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
for i in data:
    print(data[i])
'''
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


        if 'Condition' in act[name]:
            if not self.conditions(act[name]['Condition']):
                self.threadLock.acquire()
                print(str(datetime.now())+';'+self.cur+'.'+name+' Skipped' )
                self.threadLock.release()

                self.threadLock.acquire()
                print(str(datetime.now())+';'+self.cur+'.'+name+' Exit')
                self.threadLock.release()

                return
'''
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
        print(str(datetime.now())+';'+self.cur+' Entry')
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
                    t_temp = threading.Thread(target=Workflow, args = (act[j],self.cur+'.'+j,l))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    Workflow(data = act[j],cur = self.cur+'.'+j,concurrent = l)
                    #del next
        for x in threads:
            x.join()


    def exec_func(self,name,act):
        global path,ops

        func = act[name]['Function']
        inputs = act[name]['Inputs']
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.cur+'.'+name+' Entry')
        self.threadLock.release()
            
        
        if func == "TimeFunction":
            f_input = inputs['FunctionInput']
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

    
    def Finish(self):
        self.threadLock.acquire()
        print(str(datetime.now())+';'+self.cur+' Exit')
        self.threadLock.release()


dts = {}
ops = {}
path = "Milestone1"

with open('Milestone1\Milestone1B.yaml','r') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

for i in data:
    if data[i]['Execution'] =='Sequential':
        p1 = Workflow(data[i],i)
        p1.Finish()

fout = sys.stdout
f = open('M1B_output.txt', 'w')
sys.stdout = f



sys.stdout = fout
f.close()