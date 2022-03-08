import time
import pandas as pd

def TimeFunction(Executiontime):
    time.sleep(int(Executiontime))

def DataLoad(filename):
    df = pd.read_csv(filename)
    defects = len(df.index)
    return {'DataTable' : df,'NoOfDefects': defects}



def Binning(file, d):
    val = file['BIN_ID']
    con = file['RULE']

    d["Bincode"] = ""
    con = str(con)

    for r in d['Signal']:
        l = l+con.replace('Signal',str(r))+')'
        if exec(l):
            d['Bincode'] =   val

    return d

def MergeResults():
    pass

def ExportResults():
    pass

