import csv
import numpy
import scipy.stats

def open_cyrpto_file(name):
	btcFile = open(name, 'rb')
	btcData = csv.reader(btcFile)

	prevDate = 0
	prevHour = 0
	btcTemp = []
	btcHourlyData = []

	for row in btcData:
		if row[0] == "Date":
			continue
		if row[0] == prevDate:
			if row[1][:2] == prevHour:
				btcTemp.append(float(row[5]))
			else:
				# print prevDate, prevHour, numpy.mean(btcTemp)
				btcHourlyData.append(numpy.mean(btcTemp))
				if int(prevHour) + 1 != int(row[1][:2]) or (prevHour == '23' and row[1][:2] == '0'):
					btcHourlyData.append(btcHourlyData[len(btcHourlyData)-1])
				prevHour = row[1][:2] 
				btcTemp = [float(row[5])]
		else:
			# print prevDate, prevHour, numpy.mean(btcTemp)
			btcHourlyData.append(numpy.mean(btcTemp))
			prevHour = row[1][:2] 
			prevDate = row[0]
			btcTemp = [float(row[5])]

	return btcHourlyData

def percent_difference(mylist):
	outList = []
	for x in range(len(mylist)):
		try:
			outList.append((mylist[x+1] - mylist[x])/mylist[x])
		except:
			pass
	return outList

def moving_average(mylist, time):
	outList = []
	for x in range(len(mylist)):
		try:
			outList.append(numpy.sum(mylist[(x-time):(x)])/time)
		except:
			pass
	return outList[(time - 1):]

def correlation(x, y):
	xPercDiff = percent_difference(x)
	xMovAvg = moving_average(xPercDiff[1:], 24)
	yPercDiff = percent_difference(y)
	yMovAvg = moving_average(yPercDiff[1:], 24)

	return numpy.corrcoef(xMovAvg[(len(xMovAvg)-len(yMovAvg)+1):], yMovAvg[1:])

def regression(x, y):
	return scipy.stats.linregress(x[(len(x)-len(y)+1):], y[1:])

def moving_entries(x, y, lookback = 12, z_score = 1.2):
	entries = []
	for i in xrange(lookback, len(y)):
		x_mean = numpy.mean(x[len(x)-len(y)+i-lookback : len(x)-len(y)+i])
		y_mean = numpy.mean(y[i - lookback : i])
		x_std = numpy.std(x[len(x)-len(y)+i-lookback : len(x)-len(y)+i])
		#if (y_mean-x_mean)/x_std < z_score:
		if(y_mean < x_mean):
			entries.append(y[i])
	print len(entries)
	return entries

# Inputs:	Array of arithmetic returns (ex. [0.12, 0.03, -0.004, 0.02])
# Outputs:	Gross cumulative arithmetic return (ex. 1.822 means 82.2% return)
def calcCumulReturn(returns):
	cumul = 1
	for investment in returns:
		cumul = cumul * (1 + investment)
	return cumul

# Inputs:	Array of arithmetic returns (ex. [0.12, 0.03, -0.004, 0.02])
#			Array of risk free rate (ex. [.01, .02, .01, .01, .01])
#			Array of holding periods (ex. [1, 1, 3, 4, 6, 12, 2])
#			NOTE: Arrays all have to be same length!
# Outputs:	Sharpe Ratio (ex. 0.35)
def calcSharpe(returns, riskFree=.0004):
	return (numpy.mean(returns) - riskFree) / numpy.std(returns)

btc = open_cyrpto_file('btc.csv')
nmc = open_cyrpto_file('nmc.csv')
ltc = open_cyrpto_file('ltc.csv')
nvc = open_cyrpto_file('nvc.csv')
ppc = open_cyrpto_file('ppc.csv')

#----Linear Regression----#
print 'BTC - LTC : ', regression(btc, ltc)
print 'BTC - NMC : ', regression(btc, nmc)
print 'BTC - NVC : ', regression(btc, nvc)
print 'BTC - PPC : ', regression(btc, ppc)
#-------------------------#

#----Correlation----#
print 'BTC - LTC Correl ', correlation(btc, ltc)
print 'BTC - NMC Correl ', correlation(btc, nmc)
print 'BTC - NVC Correl ', correlation(btc, nvc)
print 'BTC - PPC Correl ', correlation(btc, ppc)

nmc_spread = moving_entries(percent_difference(btc), percent_difference(nmc))
print 'NMC : ', calcCumulReturn(nmc_spread), calcSharpe(nmc_spread)

ltc_spread = moving_entries(percent_difference(btc), percent_difference(ltc))
print 'LTC : ', calcCumulReturn(ltc_spread), calcSharpe(ltc_spread)

nvc_spread = moving_entries(percent_difference(btc), percent_difference(nvc))
print 'NVC : ', calcCumulReturn(nvc_spread), calcSharpe(nvc_spread)

ppc_spread = moving_entries(percent_difference(btc), percent_difference(ppc))
print 'PPC : ', calcCumulReturn(ppc_spread), calcSharpe(ppc_spread)