class Stock:
	'class stock'	
	def __int__(seft,ticker,openFixed, closeFixed,hightFixed, lowFixed, date):
		seft.ticker = ticker
		seft.openFixed = openFixed
		seft.closeFixed = closeFixed
		seft.hightFixed = hightFixed
		seft.lowFixed = lowFixed
		seft.date = date

	def getOpenFixed(seft):
		return seft.openFixed

	def getCloseFixed(seft):
		return seft.closeFixed

	def getHightFixed(seft):
		return seft.hightFixed

	def getLowFixed(seft):
		return seft.lowFixed

	def getDate(seft):
		return seft.date