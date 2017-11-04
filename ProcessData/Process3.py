from Stock import Stock
import os
import pandas as pd
import matplotlib.pyplot as plt

listStock =[]

def createDataFrame(pathFile):
    df = pd.read_csv(pathFile, index_col='<DTYYYYMMDD>')
    #print df
    return df

def fillInMissinngDate(data):
    idate = range(int(data.index.min()), int(data.index.max()))
    df1 = data.reindex(idate, columns=list(data.columns))
    lengDate = data.index.max() - data.index.min()
    print lengDate
    k = 0
    for i in range(lengDate):
        #print i
     #   print data.index[k]
      #  print df1.index[i]
        if(data.index[k] != df1.index[i]):
            #print ('i : ', i)
            #print k
            #print data.index[k]
            #print df1.index[i]
            #print df1.loc[df1.index[i],'<OpenFixed>']
            #print (data.loc[data.index[k],'<OpenFixed>'])         
            df1.loc[df1.index[i],'<OpenFixed>'] = (df1.loc[df1.index[i-1],'<OpenFixed>'] + data.loc[data.index[k],'<OpenFixed>'])/2
            df1.loc[df1.index[i],'<HighFixed>'] = (df1.loc[df1.index[i-1],'<HighFixed>'] + data.loc[data.index[k],'<HighFixed>'])/2
            df1.loc[df1.index[i],'<LowFixed>'] = (df1.loc[df1.index[i-1],'<LowFixed>'] + data.loc[data.index[k],'<LowFixed>'])/2
            df1.loc[df1.index[i],'<CloseFixed>'] = (df1.loc[df1.index[i-1],'<CloseFixed>'] + data.loc[data.index[k],'<CloseFixed>'])/2
        else:
            k = k + 1
    df1['<Ticker>'] = df1['<Ticker>'].fillna(value = data.iat[0,0])    
    return df1

def writeData(path,data):
    data.to_csv(path)

def getValueMissing(ticker,Filldate, stockDate1, stockDate2):
    valueClose = (stockDate2.getCloseFixed() + stockDate1.getCloseFixed())/2
    valueHight = (stockDate2.getHightFixed() + stockDate1.getHightFixed())/2
    valueLow = (stockDate2.getLowFixed() + stockDate1.getLowFixed())/2
    valueOpen = (stockDate2.getOpenFixed() + stockDate1.getOpenFixed())/2
    sto = Stock(ticker, valueOpen, valueClose, valueHight, valueLow, Filldate)
    return sto

def Process(pathIn, pathOut):
    file = os.listdir(pathIn)
    kq = os.listdir(pathOut)
    for f in file:
        if((f in kq) == False):    
            df = createDataFrame(pathIn+'/'+f)
            df2 = df.sort_index(axis=0, ascending=True)
            df1 = fillInMissinngDate(df2)
            writeData((pathOut+'/'+f), df1)
            print ('Done'+ f)
#getFile('./test')
#createDataFrame('./test/excel_aaa.csv')
#dataf = pd.concat(listStock)

#print dataf
#ll = fillInMissinngDate(dataf)
#writeData('./test/excel_a.csv', ll)
#plt.plot(dataf['<CloseFixed>'],dataf['<LowFixed>'])
#plt.show()
Process('./DataRaw/3', './Kq')