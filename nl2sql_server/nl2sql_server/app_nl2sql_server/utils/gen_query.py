# -*- coding: utf-8 -*-
import warnings
import json
import requests
import random
import time
import hashlib
import logging
from utils.JadpRSAUtil import get_public_key, do_encrypt
from utils import log_file

log_file(logging.INFO)

warnings.filterwarnings("ignore")

class Gen_Model():

    def __init__(self):
        with open("config.json", encoding="utf-8") as req_source:
            source = json.loads(req_source.read())
            self.url_gen = source["gen_url"][0]
            self.url_token = source["gen_url"][1]
            self.url_query = source["gen_url"][2]
            self.appId = source["appId"]
            self.appKey = source["appKey"]

    
    def sha256_encrypt(self, string):
        sha256 = hashlib.sha256()
        sha256.update(string.encode('utf-8'))
        return sha256.hexdigest()


    
    def gen_chat(self,query, gen_hist=[], ans="", generate_config={}, mode="all"):
        generate_config = {"temperature":"0.002"}
        body = {
            "messages": gen_hist,
            "generate_config": generate_config,
            "stream": True
        }
        # current_timestamp = time.time()
        # appSerct=self.appId + "UZ"+ self.appKey+ "UZ" + str(int(current_timestamp* 1000))
        # byte_str = self.sha256_encrypt(appSerct)
        # headers={"Content-Type":"application/json", "Referer":"https://ai.csg.cn/", "APP-KEY": byte_str + "." + str(int(current_timestamp*1000)), "APP-ID": self.appId}
        # response = requests.post(url=self.url_gen, json=body, headers=headers, stream=True, verify=False)
        proxies = {'http': None, 'https': None}
        response = requests.post(url=self.url_gen, json=body, stream=True, headers={'Content-type': 'application/json'}, proxies=proxies)
        response_json = {}
        response_json["query"] = query
        response_json["answer"] = response
        response_json["plot_chart"] = ans
        return response_json
    
    def query_token(self):
        date_time = time.time()
        time_a = (int)(date_time*1000)
        param = {
            "account": "dawate@csg.cn",
            "systemName": "TOP",
            "dateTime": time_a
        }
        modules = "115485327386581986190791279662517646278427866500072140597053042455611790714030464959325867921832454328355323166728504390817076224593340983784982898067533189173517162898099276509278900693864068725622068806417934055472176323464872296577664670052395406825981698590350915280738245998865080366439125047503890628359"
        public_exponent = "65537"
        param_str = json.dumps(param)
        public_key = get_public_key(modules, public_exponent)
        encrypted_message = do_encrypt(param_str, public_key)
        param = {
            "ciphertext":encrypted_message.upper()
        }
        response = requests.post(url=self.url_token, json=param, headers={'Content-type': 'application/json'})
        result_json = json.loads(response.text)
        token = ""
        if not result_json == "" and result_json['code'] == 1:
            token = result_json['token']
        return token
    
    def query_list(self, param, token):
        response = requests.post(url=self.url_query, json=param,verify = False, headers={'Content-type': 'application/json', "access-token":token})
        print(response.text)
        return response

    def __call__(self, query, gen_hist):
        return self.gen_chat(query, gen_hist)

