from dateutil.relativedelta import *
from dateutil.parser import *
from datetime import datetime
import numpy as np
import operator
import sqlite3 as lite

#Wiki Data from http://stats.grok.se/json/en/201403/Bitcoin
#Copied and pasted dictionaries from JSON
def loadWikiData():
	wikiViews = {"2014-04-16": 15873, "2014-04-17": 14818, "2014-04-14": 18614, "2014-04-12": 8570, "2014-04-13": 9081, "2014-04-10": 13714, "2014-04-11": 12052, "2014-04-18": 9270, "2014-02-07": 42980, "2014-02-06": 32561, "2014-03-28": 15466, "2014-03-29": 10666, "2014-03-22": 18444, "2014-03-23": 14978, "2014-03-20": 21017, "2014-03-21": 35209, "2014-03-26": 26670, "2014-03-27": 19029, "2014-03-24": 16444, "2014-03-25": 20792, "2014-04-05": 12088, "2014-04-04": 18836, "2014-04-07": 11701, "2014-04-06": 8585, "2014-04-01": 15652, "2014-04-03": 21833, "2014-04-02": 17688, "2014-04-21": 9974, "2014-04-09": 16313, "2014-04-08": 12165, "2014-04-15": 11884, "2014-02-09": 29662, "2014-02-08": 29728, "2014-03-31": 18816, "2014-03-30": 11798, "2014-04-28": 12312, "2014-04-27": 8579, "2014-04-26": 6992, "2014-04-19": 9070, "2014-04-25": 11577, "2014-03-08": 37941, "2014-03-09": 25017, "2014-04-29": 10689, "2014-03-04": 31175, "2014-03-05": 46115, "2014-03-06": 86464, "2014-03-07": 117065, "2014-04-23": 10486, "2014-03-01": 45034, "2014-03-02": 28527, "2014-03-03": 31447, "2014-03-13": 24156, "2014-03-12": 26685, "2014-03-11": 28188, "2014-03-10": 30437, "2014-03-17": 18270, "2014-03-16": 12204, "2014-03-15": 13037, "2014-03-14": 19513, "2014-03-19": 16598, "2014-03-18": 18328, "2014-04-24": 9806, "2014-02-28": 62430, "2014-02-25": 85468, "2014-02-24": 20316, "2014-02-27": 42162, "2014-02-26": 62266, "2014-02-21": 23061, "2014-02-20": 34802, "2014-02-23": 15393, "2014-02-22": 17682, "2014-04-22": 11402, "2014-02-10": 43543, "2014-02-11": 37538, "2014-02-12": 27779, "2014-02-13": 25169, "2014-02-14": 26753, "2014-02-15": 18419, "2014-02-16": 20078, "2014-02-17": 22452, "2014-02-18": 31507, "2014-02-19": 32556, "2014-04-20": 7261, "2014-02-05": 33076, "2014-02-04": 45364, "2014-02-03": 27526, "2014-02-02": 24345, "2014-02-01": 26883, "2014-01-31": 27584, "2014-01-30": 35048}
	wikiViews.update({"2013-08-26": 7351, "2013-08-27": 9386, "2013-08-28": 9560, "2013-08-19": 10826, "2013-08-18": 6747, "2013-08-31": 5259, "2013-08-29": 8280, "2013-08-15": 13482, "2013-08-14": 15454, "2013-08-17": 7780, "2013-08-16": 11230, "2013-08-11": 6069, "2013-08-10": 5136, "2013-08-13": 11157, "2013-08-12": 10290, "2013-08-30": 7050, "2013-08-20": 11569, "2013-08-21": 11741, "2013-08-22": 10214, "2013-08-23": 8863, "2013-08-24": 6216, "2013-08-25": 5688, "2013-08-08": 11422, "2013-08-09": 8161, "2013-08-06": 6994, "2013-08-07": 7421, "2013-08-04": 5322, "2013-08-05": 8729, "2013-08-02": 6321, "2013-08-03": 5310, "2013-08-01": 6973})
	wikiViews.update({"2013-09-09": 11338, "2013-09-22": 5497, "2013-09-21": 5655, "2013-09-20": 8648, "2013-09-27": 5907, "2013-09-26": 7292, "2013-09-25": 6212, "2013-09-24": 6695, "2013-09-01": 5153, "2013-09-03": 6740, "2013-09-02": 5971, "2013-09-05": 6929, "2013-09-04": 6438, "2013-09-07": 4828, "2013-09-06": 6808, "2013-09-28": 4707, "2013-09-30": 6682, "2013-09-31": 0, "2013-09-18": 6651, "2013-09-19": 5973, "2013-09-12": 6285, "2013-09-13": 5727, "2013-09-10": 8085, "2013-09-11": 6795, "2013-09-16": 7419, "2013-09-17": 7549, "2013-09-14": 4371, "2013-09-15": 4771, "2013-09-23": 7992, "2013-09-08": 7756, "2013-09-29": 5406})
	wikiViews.update({"2013-10-23": 11023, "2013-10-22": 8930, "2013-10-07": 14552, "2013-10-06": 11907, "2013-10-05": 15888, "2013-10-04": 26432, "2013-10-03": 49212, "2013-10-02": 20338, "2013-10-01": 6454, "2013-10-25": 10653, "2013-10-24": 9881, "2013-10-27": 18528, "2013-10-26": 15668, "2013-10-21": 8025, "2013-10-20": 6250, "2013-10-09": 12973, "2013-10-08": 13394, "2013-10-29": 43895, "2013-10-28": 18524, "2013-10-10": 10466, "2013-10-11": 8126, "2013-10-12": 5717, "2013-10-13": 5841, "2013-10-14": 7550, "2013-10-15": 8873, "2013-10-16": 8958, "2013-10-17": 8077, "2013-10-18": 9319, "2013-10-19": 6184, "2013-10-30": 74322, "2013-10-31": 113274})
	wikiViews.update({"2013-11-24": 32395, "2013-11-28": 126577, "2013-11-29": 108657, "2013-11-08": 26376, "2013-11-09": 24980, "2013-11-22": 59388, "2013-11-05": 27715, "2013-11-20": 67059, "2013-11-21": 59865, "2013-11-26": 41532, "2013-11-01": 26650, "2013-11-02": 18769, "2013-11-03": 15443, "2013-11-25": 37224, "2013-11-04": 25913, "2013-11-23": 36534, "2013-11-06": 31321, "2013-11-07": 26683, "2013-11-27": 72185, "2013-11-13": 27661, "2013-11-12": 26058, "2013-11-11": 22110, "2013-11-10": 21813, "2013-11-17": 21905, "2013-11-16": 24432, "2013-11-15": 33242, "2013-11-14": 28400, "2013-11-31": 0, "2013-11-30": 80660, "2013-11-19": 103952, "2013-11-18": 63159})
	wikiViews.update({"2013-12-29": 27988, "2013-12-28": 29142, "2013-12-23": 40699, "2013-12-22": 35461, "2013-12-21": 30786, "2013-12-20": 37054, "2013-12-27": 34917, "2013-12-26": 31107, "2013-12-25": 28606, "2013-12-24": 34495, "2013-12-01": 48325, "2013-12-03": 72379, "2013-12-02": 75136, "2013-12-05": 86851, "2013-12-04": 56600, "2013-12-07": 66393, "2013-12-06": 90565, "2013-12-09": 52953, "2013-12-08": 44535, "2013-12-31": 26160, "2013-12-30": 30416, "2013-12-12": 47245, "2013-12-13": 46321, "2013-12-10": 55541, "2013-12-11": 55913, "2013-12-16": 51107, "2013-12-17": 44891, "2013-12-14": 39090, "2013-12-15": 43715, "2013-12-18": 72543, "2013-12-19": 52637})
	wikiViews.update({"2014-01-15": 38423, "2014-01-14": 37051, "2014-01-17": 50420, "2014-01-16": 47988, "2014-01-11": 26579, "2014-01-10": 41792, "2014-01-13": 33581, "2014-01-12": 26953, "2014-01-19": 24937, "2014-01-18": 26715, "2014-01-28": 55256, "2014-01-29": 40830, "2014-01-20": 34121, "2014-01-21": 46075, "2014-01-22": 50982, "2014-01-23": 38760, "2014-01-24": 35287, "2014-01-25": 22449, "2014-01-26": 25599, "2014-01-27": 52072, "2014-01-06": 0, "2014-01-07": 39818, "2014-01-04": 22404, "2014-01-05": 4842, "2014-01-02": 27252, "2014-01-03": 30480, "2014-01-01": 23033, "2014-01-08": 39671, "2014-01-09": 40866, "2014-01-31": 27584, "2014-01-30": 35048})
	wikiViews.update( {"2014-02-23": 15393, "2014-02-07": 42980, "2014-02-06": 32561, "2014-02-05": 33076, "2014-02-04": 45364, "2014-02-03": 27526, "2014-02-02": 24345, "2014-02-01": 26883, "2014-02-25": 85468, "2014-02-24": 20316, "2014-02-27": 42162, "2014-02-26": 62266, "2014-02-21": 23061, "2014-02-20": 34802, "2014-02-09": 29662, "2014-02-22": 17682, "2014-02-29": 0, "2014-02-28": 62430, "2014-02-10": 43543, "2014-02-11": 37538, "2014-02-12": 27779, "2014-02-13": 25169, "2014-02-14": 26753, "2014-02-15": 18419, "2014-02-16": 20078, "2014-02-17": 22452, "2014-02-18": 31507, "2014-02-19": 32556, "2014-02-08": 29728, "2014-02-30": 0, "2014-02-31": 0})
	return wikiViews

class Cryptocurrency():
	"""
	:Overview: Intraday dataset of btc, ltc, nmc, and nvc
	"""
	def __init__(self, ticker):
		"""
		:Construction: input Crypto-ticker (current valid = ltc, nmc, btc, nvc)
		"""

		self.ticker = ticker
		self.db = lite.connect('bitcoin.db')
		self.cursor = self.db.cursor()

	def getDailyValues(self, startDate, endDate=datetime.now(), column = 'last'):
		"""
		:Inputs: start and end times
		:Output: dictionary of average daily values in time range
		"""
		self.avgDailyDic = {}
		self.cursor.execute('select strftime("%Y-%m-%d", timestamp), avg(' + column + ') from ' + str(self.ticker) + ' where timestamp > "' + str(startDate) + '" AND timestamp < "' + str(endDate) + '" group by strftime("%Y-%m-%d", timestamp)')
		hist = self.cursor.fetchall()
		for row in hist:
			self.avgDailyDic[row[0]] = row[1]
		return self.avgDailyDic

	def getHourlyValues(self, startDate, endDate=datetime.now()):
		"""
		:Inputs: start and end times
		:Output: dictionary of average hourly values in time range
		"""
		self.ticks = {}
		self.cursor.execute('select strftime("%Y-%m-%d %H:00:00", timestamp), avg(last) from ' + str(self.ticker) + ' where timestamp > "' + str(startDate) + '" AND timestamp < "' + str(endDate) + '" group by strftime("%Y-%m-%d %H", timestamp)')
		hist = self.cursor.fetchall()
		for row in hist:
			self.ticks[row[0]] = float(row[1])
		return self.ticks


	def getHourlyRandValues(self, startTime, endTime=datetime.now()):
		self.ticks = {}
		self.cursor.execute('select strftime("%Y-%m-%d %H:00:00", timestamp), last from ' + str(self.ticker) + ' where timestamp > "' + str(startTime) + '" AND timestamp < "' + str(endTime) + '"')
		hist = self.cursor.fetchall()
		for row in hist:
			self.ticks[row[0]] = float(row[1])
		return self.ticks

	def get5MinuteValues(self, startDate, endDate=datetime.now()):
		"""
		:Inputs: start and end times
		:Output: dictionary of average values at 5 minute intervals in time range
		"""
		self.avgHourlyDic = {}
		self.cursor.execute('select strftime("%Y-%m-%d %H:00:00", timestamp), avg(last) from ' + str(self.ticker) + ' where timestamp > "' + str(startDate) + '" AND timestamp < "' + str(endDate) + '" group by strftime("%Y-%m-%d %H", timestamp)')
		hist = self.cursor.fetchall()
		for row in hist:
			self.avgHourlyDic[row[0]] = row[1]
		return self.avgHourlyDic

	def getValue(self, timestamp):
		try:
			return self.ticks[timestamp]
		except:
			pass
			#raise Exception('Key ' + str(timestamp) + ' not found')
