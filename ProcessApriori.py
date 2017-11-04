import csv
from collections import defaultdict
from itertools import chain, combinations

#read file csv contains transtion
def readFile(path):
	f = open(path, 'r')
	with f:
	    reader = csv.reader(f)
	    for row in reader:
        	line = frozenset(row)
        	yield line
        	
#get  list transtion and itemset which codestock     	
def getTransListAItemSet(data):
	transactionList = list();
	itemSet = set();
	for trans in data:
		transaction = frozenset(trans)
		transactionList.append(transaction)
		for item in transaction:
			item = frozenset([item])
			itemSet.add(item)
	return transactionList, itemSet

#get item with support >=  value min support
def getItemsWithSup(itemSet, transactionList, minSup, freqItem):
	items = set()
	for item in itemSet:
		for trans in transactionList:
			if(item.issubset(trans)):
				freqItem[item] = freqItem[item] + 1

	for item in itemSet:																																																																																																		
		if(getSup(item, freqItem, transactionList) >= minSup):
			items.add(item)
			
	return items

#get value support of item
def getSup(item, freqItem, transList):
	return float(freqItem[item])/len(transList)

def getConFi(item, freqItem, transList):
	return 1

def getLift(item, freqItem, transList):
	return 1

def joinItemSet(itemSet, lenght):
	return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == lenght])

def getItemsSetWithFred(largItem, freqItem,transList):
	ItemFred = []
	for key,value in largItem.items():
		#ssprint value
		ItemFred.extend([(tuple(item), getSup(item, freqItem, transList))
                           for item in value])
                           
	return ItemFred

def getSubSets(arr):
	return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def getRule(largItem, freqItem, transList, minConf):
	Rules = []
	for dex, value in largItem.items():
		for item in value:
			_subsets = map(frozenset, [x for x in getSubSets(item)])
			for element in _subsets:
				remain = item.difference(element)
				if len(remain) > 0:
					confidence = getSup(item, freqItem,transList)/getSup(element, freqItem, transList)
					#print confidence
					if confidence >= minConf:
						Rules.append(((tuple(element), tuple(remain)), confidence))
	return Rules

def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
	
    for item, support in items: 
        print "item: %s , %.3f" % (str(item), support)
    print '-----------------------------------------'
    for r, confi in rules:
    	pre, after = r
    	print "Rule: %s ==> %s , %.3f" % (str(pre), str(after), confi)

def Apriori(data, minSup, minConfi):

	transList, itemSet = getTransListAItemSet(data)
	freqItem = defaultdict(int)
	largItem = dict()
	Rules = dict()
	k = 2
	currentLSet = getItemsWithSup(itemSet,transList,minSup,freqItem)
	#print currentLSet
	while(currentLSet != set([])):
		#print k
		#k = k +1
		largItem[k-1] = currentLSet
		currentLSet = joinItemSet(currentLSet, k)
		currentCSet = getItemsWithSup(currentLSet,transList,minSup,freqItem)
		k = k+1
		currentLSet = currentCSet
        
	return getItemsSetWithFred(largItem, freqItem, transList), getRule(largItem, freqItem,transList, minConfi)

	#print freqItem
	


datas = readFile('./ResultNotProcessData/ResultCluster.csv')	
#tr,it = getTransListAItemSet(datas)
#fred = defaultdict(int)
#print getItemBigSup(it,tr,0.3,fred)
#print tr

it, r = Apriori(datas ,0.5,0.6)

printResults(it,r)
#print joinItemSet(it,2)
