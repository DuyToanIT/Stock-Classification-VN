import os
import pandas as pd
import matplotlib.pyplot as plt

def createDataFrame(pathFile):
    df = pd.read_csv(pathFile, index_col='<DTYYYYMMDD>')
    #print df
    return df

def writeData(path,data):
    data.to_csv(path)

def Process(pathIn, pathOut):
    file = os.listdir(pathIn)
    i = 1
    k = 1
    for f in file:    
        df = createDataFrame(pathIn+'/'+f)
        if(i ==  100):
        	k = k +1
        	i = 0
        i = i +1	
        writeData((pathOut+'/'+str(k)+'/'+f), df)

Process('./Data', './DataRaw')