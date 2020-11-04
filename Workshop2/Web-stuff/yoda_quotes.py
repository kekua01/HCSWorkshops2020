import requests
from bs4 import BeautifulSoup

page = requests.get("https://wiselifelesson.com/yoda-quotes/")
soup = BeautifulSoup(page.content, 'html.parser')

quotes = soup.select('p strong')

i = 1
#there were a few random quotes at the bottom, so I've hardcoded in the 101
while i <= 101:
	print (str(i) + '.  ' + quotes[i].get_text() + '\n')
	i += 1