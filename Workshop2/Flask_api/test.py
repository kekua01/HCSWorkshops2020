import requests

BASE = "http://127.0.1:5000/"

data = [{"likes": 10, "name": "Coby", "views": 1000}, 
		{"likes": 15, "name": "The best video", "views": 300}, 
		{"likes": 43, "name": "The worst video", "views": 1440}]

for i in range(len(data)):
	response = requests.put(BASE + "video/" + str(i), data[i])
	print(response.json())

input()
reponse = requests.get(BASE + "video/6")
print(response.json())