import yaml
import pandas as pd
import multiprocessing as mp
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

def exec(x,activity,str_template,txt_lines):
    task = activity[x]
    str_template.append(x)
    line = log_file(str_template) + " Entry\n"
    txt_lines.append(line)
    task_attr = list(task.keys())
    # change to required conditional expression
    condition = 1
    if "Execution" in task_attr:
        sub_flow = task['Activities']
        act_on_activities(sub_flow, str_template, txt_lines)
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

#here the activities are parsed
def act_on_activities(activity, str_template, txt_lines,flag):
    
    #parsing the activities to execute them
    list_tasks = list(activity.keys())
    if flag == 0:
        for x in list_tasks:
            exec(x,activity,str_template,txt_lines)
    else:
        process=[]
        for x in list_tasks:
            p = mp.Process(target= exec,args=(x,activity,str_template,txt_lines))
            p.start()
            process.append(p)
        for p in process:
            p.join()
            

    
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
                if activity['Execution'] == 'Sequential':
                    flag = 0
                else:
                    flag = 1
                act_on_activities(activity, str_template, txt_lines,flag)
                task_string = log_file(str_template) + " Exit\n"
                txt_lines.append(task_string)
                log_file.writelines(txt_lines)
                print("Workflow {} has been logged".format(x))
            print("File Created!")
            log_file.close()