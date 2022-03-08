import time
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

