import time
#from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import pandas as pd
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import easyquotation
import urllib.request
import itertools



scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)
sheet = client.open('CPB batch checker').worksheet("Sheet1")


def next_available_row(worksheet, i):
    str_list = list(filter(None, worksheet.col_values(i)))
    return len(str_list)+1

def permutations_with_replacement(dic, k):
	result=[]
	for i in itertools.product(dic, repeat=k):
		result.append(''.join(i))
	return result


if __name__ == "__main__":
	url = 'https://cosmetic.momoko.hk/calculate.php'
	nextrow = next_available_row(sheet,2)

	print('start checking')
	first100 = []
	first1000comb = sheet.col_values(1)
	first_col_last_row = next_available_row(sheet,1)-1

	for j in range(10000):
		for i in range(nextrow+10-1,nextrow+10-1+10):
			print('j: '+str(j) + ',i: ' + str(i))
			myobj = {'brand':'C18', 'code':first1000comb[i-1]}
			print(myobj['code'])
			y = requests.post(url, data=myobj)
			x = y.json()
			if x['status'] != 'OK':
				first100.append(['X'])
				if i==next_available_row(sheet,2)+10-1:
					sheet.update('b'+str(nextrow)+':b'+str(nextrow+10-1),first100)
					first100=[]
				continue
			first100.append([x['date']])
			if i==nextrow+10-1:
				sheet.update('b'+str(2)+':b'+str(nextrow+10-1),first100)
				first100=[]








	# print('start checking')
	# first100 = []
	# first_col_last_row = next_available_row(sheet,1)-1
	# for i in range(next_available_row(sheet,2),first_col_last_row):
	# 	print('checking ' + str(sheet.cell(i,1).value))
	# 	myobj = {'brand':'C18', 'code':sheet.cell(i,1).value}
	# 	y = requests.post(url, data=myobj)
	# 	x = y.json()
	# 	if x['status'] is not 'OK':
	# 		sheet.update_cell(i,2,'X')

	# 		time.sleep(2.1)
	# 		continue
	# 	sheet.update_cell(i,2,x['date'])
	# 	print(x['date'])
	# 	time.sleep(2.1)

# {"status":"OK","title":"CDP - cl\u00e9 de peau","code":"3RNQU","date":"Dec 2020"}

		# {"status":"E","title":"CDP - cl\u00e9 de peau","error":"<p>The batch code you entered is invalid.
		# <\/p><p>cl\u00e9 de peau's 4 to 6 characters batch code (e.g. NZ17, 3PNTU, 6230UA) is usually 
		# printed or stamped on the body or bottom of the packaging.<\/p>"}
