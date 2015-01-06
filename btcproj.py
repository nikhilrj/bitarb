from dbLoad import *
import matplotlib.pyplot as plt
import datetime
import numpy


def dateSeries(startDate, endDate):
	dt = parse(startDate)
	end = parse(endDate)
	step = datetime.timedelta(days=1)

	result = []

	while dt < end:
		result.append(dt.strftime('%Y-%m-%d'))
		dt += step

	return result

def returns(dic, days):
	return [np.log(dic[days[i]]/dic[days[i-1]]) for i in xrange(1,len(days))]



startDate = '2013-09-01'
endDate = '2014-02-01'
c = Cryptocurrency('btc')

prices = c.getDailyValues(startDate, endDate)
wikiData = loadWikiData()
days = dateSeries(startDate, endDate)
wikiSlice = [wikiData[i] for i in days]

try:
	while wikiSlice.index(0) >= 1:
		wikiSlice[wikiSlice.index(0)]+=wikiSlice[wikiSlice.index(0)-1]
except:
	pass

wikiDel = [float((wikiSlice[i] - wikiSlice[i-1]))/wikiSlice[i-1] for i in xrange(1, len(days))]
rets = returns(prices)

print numpy.correlate(rets, wikiDel)