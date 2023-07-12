import requests
import json

# https://api.stackexchange.com/docs
# https://api.stackexchange.com/docs/questions

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')

#print(response)
#print(response.json()["items"])

for data in response.json()["items"]:
    if data["answer_count"] == 0:
        print(data["title"])
        print(data["link"])
    else:
        print("skipped")