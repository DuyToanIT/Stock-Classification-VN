#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 10:20:36 2017

@author: duytoan
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

listStock = []
def readData(pathFolder):
    folder = os.listdir(pathFolder)
    for file in folder:
        df = pd.read_csv(pathFolder+'/'+file)
        listStock.append(df)
    data = pd.concat(listStock)
    return data

def drawPltBar(df, minDate, maxDate):
    df2 = df.loc[df['<DTYYYYMMDD>'] <= maxDate]
    df2 = df2.loc[df2['<DTYYYYMMDD>'] >= minDate]
    dateCounts = pd.value_counts(df2['<DTYYYYMMDD>'])
    dateCounts = dateCounts.sort_index(ascending = True)
    localX = np.arange(len(dateCounts.index))#dateCounts.index  
    laberX = dateCounts.index.tolist()
    plt.bar(localX, np.array(dateCounts.values), align='center')
    plt.xticks(localX, laberX)
    plt.xlabel('Date')
    plt.ylabel('Count stock')
    plt.show()

def filterNoise(df,percentNoise):
    minDate = df['<DTYYYYMMDD>'].min()
    maxDate = df['<DTYYYYMMDD>'].max()
    numDate = maxDate - minDate
    countTicker = pd.value_counts(df['<Ticker>'])
    listTicker = []
    for i in range(len(countTicker)):
        if((float(countTicker.values[i])/numDate) > percentNoise):
            listTicker.append(countTicker.index[i])
    
    df2 = df[df['<Ticker>'].isin(listTicker)]
    return df2

def fillMissingDate(data, minDate, maxDate):
    idate = range(minDate, maxDate+1)
    lenDate = maxDate - minDate + 1
    df1 = data.reindex(idate, columns=list(data.columns))
    df1['<Ticker>'] = df1['<Ticker>'].fillna(value = data.iat[0,0])    
    df1 = df1.fillna(value = 0)
    data = data.set_index('<DTYYYYMMDD>')
    data = data.sort_index(ascending = True)
    lenDateData = len(data.index.values)
    posData = 0
    posdf1 = 0
    while(posdf1 < lenDate):
        if(data.index[posData] == df1.index[posdf1]):
            df1.loc[df1.index[posdf1],'<DTYYYYMMDD>'] = df1.index[posdf1]
            df1.loc[df1.index[posdf1],'<OpenFixed>'] = data.loc[data.index[posData],'<OpenFixed>']
            df1.loc[df1.index[posdf1],'<HighFixed>'] = data.loc[data.index[posData],'<HighFixed>']
            df1.loc[df1.index[posdf1],'<LowFixed>'] = data.loc[data.index[posData],'<LowFixed>']
            df1.loc[df1.index[posdf1],'<CloseFixed>'] = data.loc[data.index[posData],'<CloseFixed>']
            if(posData < lenDateData -1):
                posData = posData+1
            #print ['posData'+str(posData)]
        else:
            df1.loc[df1.index[posdf1],'<DTYYYYMMDD>'] = df1.index[posdf1]
            df1.loc[df1.index[posdf1],'<OpenFixed>'] =(data.loc[data.index[posData],'<OpenFixed>'] + df1.loc[df1.index[posdf1-1],'<OpenFixed>'])/2
            df1.loc[df1.index[posdf1],'<HighFixed>'] = (data.loc[data.index[posData],'<HighFixed>'] + df1.loc[df1.index[posdf1],'<HighFixed>'])/2
            df1.loc[df1.index[posdf1],'<LowFixed>'] = (data.loc[data.index[posData],'<LowFixed>'] + df1.loc[df1.index[posdf1],'<LowFixed>'])/2
            df1.loc[df1.index[posdf1],'<CloseFixed>'] = (data.loc[data.index[posData],'<CloseFixed>'] + df1.loc[df1.index[posdf1],'<CloseFixed>'])/2
        posdf1 = posdf1 +1
        #print ['posdf1'+str(posdf1)]
    return df1

def writeData(path,data):
    data.to_csv(path,index = False)

def Process(pathIn, pathOut,minDate,maxDate,percentNoise):
    df = readData(pathIn)
    dfFilter = df.loc[df['<DTYYYYMMDD>'] <= maxDate]
    dfFilter = dfFilter.loc[dfFilter['<DTYYYYMMDD>'] >= minDate]
    dfFilter = filterNoise(dfFilter,percentNoise)
    listTicker = frozenset(dfFilter['<Ticker>'])
    for index, value in enumerate(listTicker):
        print value
        dfTicker = dfFilter.loc[dfFilter['<Ticker>'] == value]
        #dfTicker = dfTicker.set_index('<DTYYYYMMDD>')
        #df2 = dfTicker.sort_inx(axis=0, ascending = True)
        df2 = fillMissingDate(dfTicker, minDate, maxDate)
        writeData((pathOut+'/'+value+'.csv'),df2)
        print ['Done '+value]
"""
df = readData('./Data')
min = df['<DTYYYYMMDD>'].min()
max = df['<DTYYYYMMDD>'].max()
drawPltBar(df,min,max)
"""
Process('./Data','./DataProcessed',20100131,20101231,0.1)

