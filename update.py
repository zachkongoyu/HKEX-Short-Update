import requests
from bs4 import BeautifulSoup
from datetime import date
import time

url = 'https://www.hkex.com.hk/Services/Trading/Securities/Securities-Lists/Designated-Securities-Eligible-for-Short-Selling?sc_lang=en'
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

today = date.today().strftime("%d/%m/%Y")
lastUpDate = soup.find_all("td", class_='ms-rteTableEvenCol-2')[0].text.strip()

print(f"today is {today} and last update is {lastUpDate}.")

if today != lastUpDate:
	print('No update. Closing...')
	time.sleep(3)

else:
	print("An update found.")
	change = soup.find_all("td", class_='ms-rteTableEvenCol-2')[1].text.strip()
	print(change)
	if 'Add' in change:
		print("\'Add\' is detected. Now processing...")

		amount = change.split()[-1]

		new = soup.find_all("td", class_='ms-rteTableOddCol-2')[0].text.strip().split('/')
		old = soup.find_all("td", class_='ms-rteTableOddCol-2')[2].text.strip().split('/')

		new = "".join([new[i] for i in range(len(new)-1, -1, -1)])
		old = "".join([old[i] for i in range(len(old)-1, -1, -1)])

		urlNew = f'https://www.hkex.com.hk/eng/market/sec_tradinfo/ds{new}.htm'
		urlOld = f'https://www.hkex.com.hk/eng/market/sec_tradinfo/ds{old}.htm'
		soupNew = BeautifulSoup(requests.get(urlNew).content, 'html.parser')
		soupOld = BeautifulSoup(requests.get(urlOld).content, 'html.parser')

		rowsNew = []

		for j in soupNew.find_all('p', class_='MsoNormal'):
			try:
				rowsNew.append(j.find_all('span', style='font-size:9.0pt;font-family:"Verdana","sans-serif"')[0].text.strip())
			except:
				pass

		rowsNew = [(rowsNew[i+1:i+3]) for i in range(0, len(rowsNew), 4)]

		rowsOld = []

		for k in soupOld.find_all('p', class_='MsoNormal'):
			try:
				rowsOld.append(k.find_all('span', style='font-size:9.0pt;font-family:"Verdana","sans-serif"')[0].text.strip())
			except:
				pass

		rowsOld = [(rowsOld[i+1:i+3]) for i in range(0, len(rowsOld), 4)]

		unique = [row for row in rowsNew if row not in rowsOld]

		with open("C:/Users/rtamc-F/Desktop/HKEX Short Update/short tickers.txt", 'a') as f:
			f.write(lastUpDate + " Add " + amount)
			f.write('\n')
			for row in unique:
				f.write('\t')
				f.write(str(row))
				f.write('\n')

print('Done')
time.sleep(3)