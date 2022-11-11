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

url = 'https://cosmetic.momoko.hk/calculate.php'

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)
sheet = client.open('CPB batch checker').worksheet("Sheet1")


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+1

def permutations_with_replacement(dic, k):
	result=[]
	for i in itertools.product(dic, repeat=k):
		result.append(''.join(i))
	return result


if __name__ == "__main__":
	dic='abcdefghijklmnopqrstuvwxyz0123456789'
	result = permutations_with_replacement(dic,5)
	nextrow = next_available_row(sheet)
	last_row_content = sheet.cell(nextrow-1, 1).value
	print(last_row_content)
	print(result[4187])
	lastResult = result.index(last_row_content)

	for i in result[lastResult+1:]:
		sheet.update_cell(nextrow,1,i)
		nextrow=nextrow+1
		print('updating ' + str(i))
		time.sleep(2.1)