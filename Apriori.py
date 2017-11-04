from collections import defaultdict
from itertools import chain, combinations
import csv
class Apriori(object):
	"""docstring for Apriori"""
	def __init__(self, transactionList, minSup, minConf):
		self.transactionList = transactionList
		self.minSup = minSup
		self.minConf = minConf
		self.freqItem = defaultdict(int)
		self.largeItem = dict()

	def joinSubItem(self,itemsSet, lenght):
		_itemSet = set()
		for i in itemsSet:
			for j in itemsSet:
				if(len(i.union(j)) == lenght):
					_itemSet.add(i.union(j))

		return _itemSet

	def getItemsSet(self):
		_itemSet = set()
		for transaction in self.transactionList:
			_itemSet.add(frozenset([transaction]))
		return _itemSet

	def getMinSup(self):
		return self.minSup

	def getMinConf(self):
		return self.minConf

	def getTransactionList(self):
		return self.transactionList

	def getFreqItem(self):
		return self.freqItem

	def getLargeItem(self):
		return self.largeItem

	def calFreqItem(self,item):
		for transaction in self.getTransactionList():
			if(item.issubset(transaction)):
				self.getFreqItem()[item] += 1

	def calFreq(self,itemSet):
		for item in itemSet:
			self.calFreqItem(item)

	def getSup(self, item):
		return float(self.getFreqItem()[item])/len(self.transactionList)

	def getItemSetWithSup(self, itemsSet):
		_itemSet = set()
		for item in itemsSet:
			if(self.getSup(item) >= self.getMinSup()):
				_itemSet.add(item)
		return _itemSet

	def getSubSets(self,arr):
		return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

	def getRules(self):
		Rules = []
		for i, value in self.getLargeItem().items():
			print value
			for item in value:
				_subsets = map(frozenset, [x for x in self.getSubSets(item)])
				for element in _subsets:
					remain = item.difference(element)
					if len(remain) > 0:
						confidence = self.getSup(item)/self.getSup(element)
						lift = confidence/self.getSup(remain)
						sup = self.getSup(value)
					#print confidence
						if confidence >= self.getMinConf():
							Rules.append(((tuple(element), tuple(remain)), sup,confidence, lift))
		return Rules

	def infoRules(self, rule):
		print rule

	
	def run(self):
		itemsSet = self.getItemsSet()
		print itemsSet
		self.calFreq(itemsSet)
		itemsSet = self.getItemSetWithSup(itemsSet)
		k = 2
		while(itemsSet != set([])):
			itemSubSet = self.joinSubItem(itemsSet,k)
			self.calFreq(itemSubSet)
			itemsSet = self.getItemSetWithSup(itemsSet)
		print self.getRules()

def readFile(path):
	f = open(path, 'r')
	with f:
		reader = csv.reader(f)
	   	for row in reader:
			line = frozenset(row)
       		yield line

def test():
	datas = readFile('./ResultNotProcessData/ResultCluster.csv')
	transactionList = list();
	for trans in datas:
		#transaction = frozenset(trans)
		transactionList.append(trans)

	a = Apriori(transactionList, 0.2, 0.3)
	a.run()		

test()