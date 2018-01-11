import os
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import csv
import matplotlib.pyplot as plt


listStock =[]
listCluster = []
listTicker=[]
dataf = pd.DataFrame()

#Read data of multiple file csv, and return list frame data
def getDataFiles(path):
    listDataFile = []
    files = os.listdir(path)
    for f in files:
        datafile = readFile(path+'/'+f)
        listDataFile.append(datafile)
     
    return listDataFile

def createDataFrame(pathFile):
    df = pd.read_csv(pathFile)
    listStock.append(df)
# Read a file csv return dataframe
def readFile(pathFile):
    df = pd.read_csv(pathFile)
    a=pathFile.split('_',1)
     
    b=a[1].split('.')
    listTicker.append(b[0])      
    return df
                                    
# Write data for each cluster
def getCluster(pathOut, dataframe,kmean):
    #seri = ['<DTYYYYMMDD>','<Ticker>', '<OpenFixed>', '<HighFixed>','<LowFixed>', '<CloseFixed>']
    for i in range(kmean.n_clusters):
        for k in np.where(kmean.labels_ == i):
            dataframe.iloc[k,:].to_csv((pathOut+'/Cluster' +str(i)+'.csv'), index = False)
            

def writeResultCLuster():
    for i in range(len(listCluster)):
    #print listCluster[0]
        data = pd.concat(listCluster[i], ignore_index = True)
        #print data
        data.to_csv(('Cluster' +str(i)+'.csv'), index = False)
    
# Calculate percent rise by result subtraction > 0
def getPercentRise(listnum1, listnum2):
    result = map(subtraction, listnum1, listnum2)
    countElementRise = len([index for index, e in enumerate(result) if e >= 0])
    if(len(result) > 0):
        percent = float(countElementRise)/len(result)*100
    else:
        percent = 50
    return percent

# return result num1 subtraction num2
def subtraction(num1, num2):
    return (num1 - num2)

#get list ticket which have in dataframe
def getListTicket(datafram):
    return set(datafram['<Ticker>'])

#Result percent each caltogary in cluser
def resultPercentages(pathCluster, pathOut):
    listPercent = []
    df = pd.read_csv(pathCluster)
    listTicket = getListTicket(df)
    for item in listTicket:
        transTicket = df[df['<Ticker>'].isin([item])]
        valueClose = np.array(transTicket['<CloseFixed>']).tolist()
        listNum1 = list(valueClose)
        listNum2 = list(valueClose)
        listNum1.pop()
        listNum2.remove(valueClose[0])
        percent = getPercentRise(listNum1, listNum2) 
        listPercent.append((item,percent))
    print 'Done Caculator'

    arr = np.array(listPercent)
    ticker =arr[:,0]
    percentRise = arr[:,1]
    percentFall = [100 - float(x) for x in percentRise]
    np.savetxt(pathOut, np.column_stack((ticker, percentRise, percentFall)), fmt = '%s', header = "Ticker, PercentRise,PercentFall", delimiter= ",")
    print 'Done Write'
    
def processKmeans(pathOut,dataframe, ncluster, datafit):
    kmean = KMeans(n_clusters = ncluster).fit(datafit)
    for i in range(ncluster):
        for k in np.where(kmean.labels_ == i):
            dataframe.iloc[k,:].to_csv((pathOut+'/Cluster' +str(i)+'.csv'), index = False)
    return kmean.labels_, kmean.cluster_centers_

#get index of Ticker
def findpositionTicker(st):
    return listTicker.index(st.lower())

#Translate Ticker for index
def translate(arr):
    for i in arr:
        a= i[0]
        index=findpositionTicker(a)+1
        i[0]=index
    return arr    

def process(pathData):

    listFrame = getDataFiles(pathData)
    df = pd.concat(listFrame,ignore_index=True)
    print 'Done read data'

    arr = np.array(df.loc[:,['<Ticker>','<Close>']])
    # translate Ticker for Index
    arr=translate(arr)
    arr[:,0] = 0
     
    label1, center1 = processKmeans('./Result/DataProcessed/2009',df,2, arr)
    print 'Done Process Kmean'
    
    #plt.figure(figsize = (12,12))
    #plt.subplot(221)
    plt.scatter(arr[:,0],arr[:,1], c= label1)
    plt.scatter(center1[:,0], center1[:,1], marker = "x")
    plt.title('Close')
    plt.show()
     

process('./DataProcessed/2009')
#resultPercentages('./Result/NotPreProcessData/Cluster0.csv', './Result/NotPreProcessData/PercentClu0.csv')
#resultPercentages('./Result/NotPreProcessData/Cluster1.csv', './Result/NotPreProcessData/PercentClu1.csv')

