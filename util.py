import time
import cv2
import pandas as pd

def TimeFunction(Executiontime):
    time.sleep(int(Executiontime))

def DataLoad(filename):
    df = pd.read_csv(filename)
    defects = len(df.index)
    return {'DataTable' : df,'NoOfDefects': defects}

def Binning():
    pass

def MergeResults():
    pass

def ExportResults():
    pass

def create_csv(name,l):
    l = list(l)
    df = pd.DataFrame.from_records(l)
    df.to_csv((name+'.csv'), header=False, index=False)
