import time
import cv2
import pandas as pd

def TimeFunction(Executiontime):
    time.sleep(Executiontime)

def DataLoad(str: input):
    cv2.imread(input)

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
