# -*- coding: utf-8 -*-
import requests
import json

# url = "http://10.10.65.158:63000/nl2sql"

param = {
    "query":"2023年上半年广东和广西营业收入利润率是多少，广东比广西高多少"
}
response = requests.post(url="http://10.10.65.158:63000/nl2sql", json=param, headers={'Content-type': 'application/json'})

for chunk in response.iter_content(1024):
    print(chunk.decode("utf-8", "ignore"), end="")
# print("----------------", response.text)