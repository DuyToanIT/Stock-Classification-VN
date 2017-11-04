import os
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import csv
import matplotlib.pyplot as plt


listStock =[]
listCluster = []
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
    #print df
    listStock.append(df)
# Read a file csv return dataframe
def readFile(pathFile):
    df = pd.read_csv(pathFile)
    return df

def getClusterTicket():
    
    with open('ResultClusterNotProcess.csv','w') as file:
        wr = csv.writer(file)
        for i in range(kmean.n_clusters):
            listTemp = []
            for k in np.where(kmean.labels_ == i):
                str =""
                for row in k:
                    listTemp.append(dataf.at[row,'<Ticker>'])
                #print listTemp
                wr.writerow(listTemp)
                                    
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
    df = readFile(pathCluster)
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
def getXY(datafram):
    print ''        

def getDFWithMonth(fromMonth, toMonth):
    print ''
    
def processKmeans(pathOut,dataframe, ncluster, datafit):
    kmean = KMeans(n_clusters = ncluster).fit(datafit)
    for i in range(ncluster):
        for k in np.where(kmean.labels_ == i):
            dataframe.iloc[k,:].to_csv((pathOut+'/Cluster' +str(i)+'.csv'), index = False)
    return kmean.labels_, kmean.cluster_centers_

def process(pathData):
    listFrame = getDataFiles(pathData)
    df = pd.concat(listFrame, ignore_index = True)
    print 'Done read data'

    arr = np.array(df.loc[:,['<LowFixed>','<LowFixed>']])
    label1, center1 = processKmeans('./Result/DataProcessed/Low_Low',df,2, arr)
    #label1 = np.array(label1)
    plt.figure(figsize = (12,12))
    
    plt.subplot(221)
    plt.scatter(arr[:,0],arr[:,1], c= label1)
    plt.scatter(center1[:,0], center1[:,1], marker = "x")
    plt.title('Low-Low')

    arr2 = np.array(df.loc[:,['<CloseFixed>','<CloseFixed>']])
    label2,center2 = processKmeans('./Result/DataProcessed/Close_Close',df,2, arr2)
    plt.subplot(222)
    plt.scatter(arr2[:,0],arr2[:,1], c= label2)
    plt.scatter(center2[:,0], center2[:,1], marker = "x")
    plt.title('Close-Close')

    arr3 = np.array(df.loc[:,['<CloseFixed>','<LowFixed>']])
    label3, center3 = processKmeans('./Result/DataProcessed/Close_Low',df,2, arr3)
    plt.subplot(223)
    plt.scatter(arr3[:,0],arr3[:,1], c= label3)
    plt.scatter(center3[:,0], center3[:,1], marker = "x")
    plt.title('Close-Low')

    arr4 = np.array(df.loc[:,['<LowFixed>','<CloseFixed>']])
    label4, center4 = processKmeans('./Result/DataProcessed/Low_Close',df,2, arr4)
    plt.subplot(224)
    plt.scatter(arr4[:,0],arr4[:,1], c= label4)
    plt.scatter(center4[:,0], center4[:,1], marker = "x")
    plt.title('Low-Close')
    plt.show()

process('./DataProcessed')
#resultPercentages('./Result/NotPreProcessData/Close_Close/Cluster0.csv', './Result/NotPreProcessData/Close_Close/PercentClu0.csv')
#resultPercentages('./Result/NotPreProcessData/Close_Close/Cluster1.csv', './Result/NotPreProcessData/Close_Close/PercentClu1.csv')
#resultPercentages('./Result/NotPreProcessData/Close_Low/Cluster0.csv', './Result/NotPreProcessData/Close_Low/PercentClu0.csv')
#resultPercentages('./Result/NotPreProcessData/Close_Low/Cluster1.csv', './Result/NotPreProcessData/Close_Low/PercentClu1.csv')
#resultPercentages('./Result/NotPreProcessData/Low_Close/Cluster0.csv', './Result/NotPreProcessData/Low_Close/PercentClu0.csv')
#resultPercentages('./Result/NotPreProcessData/Low_Close/Cluster1.csv', './Result/NotPreProcessData/Low_Close/PercentClu1.csv')
#resultPercentages('./Result/NotPreProcessData/Low_Low/Cluster0.csv', './Result/NotPreProcessData/Low_Low/PercentClu0.csv')
#resultPercentages('./Result/NotPreProcessData/Low_Low/Cluster1.csv', './Result/NotPreProcessData/Low_Low/PercentClu1.csv')
