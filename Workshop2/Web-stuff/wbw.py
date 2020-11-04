from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

req = Request('https://waitbutwhy.com/archive', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')


posts_all = {}
posts = soup.find_all(class_='post-right')
for post in posts:
	get_title = list(post.children)[1]
	title = get_title.get_text().strip()

	get_comments = list(post.children)[3]
	comments = get_comments.get_text()
	temp = [s for s in comments.split() if s[0].isdigit()]
	num_comments = int(temp[-1].replace(',', ''))
	posts_all[title] = num_comments

posts_ordered = sorted(posts_all.items(), key=lambda x: x[1], reverse=True)

for item in posts_ordered:
	print(item[0] + ' - ' + str(item[1]) + '\n')


# print(posts2.get_text().strip())

# comms2 = comms.get_text().replace('Facebook', '')
# print(comms2.strip())
