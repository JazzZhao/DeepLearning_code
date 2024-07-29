import pandas as pd
import requests
import json
import tool
from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(max_workers=200)

zhuzhiid = pd.read_excel('./人资组织id.xlsx')
tool.clean_df(zhuzhiid)
zhuzhi_name = zhuzhiid['组织名称'].tolist()
zhuzhi_id = zhuzhiid['人资组织ID'].tolist()

dfs = pd.read_excel('./123.xlsx')
indCodes = dfs['指标编码'].tolist()
periodTypes = dfs['时间'].tolist()
indexName = dfs['指标名称'].tolist()
shujuxiang = dfs['数据项'].tolist()


import warnings
import json
import requests
import random
import time
import logging
from JadpRSAUtil import get_public_key, do_encrypt
# from utils import log_file

# log_file(logging.INFO)

warnings.filterwarnings("ignore")

class Gen_Model():

    def __init__(self):
        with open("../config.json", encoding="utf-8") as req_source:
            source = json.loads(req_source.read())
            self.url_gen = source["gen_url"][0]
            self.url_token = source["gen_url"][1]
            self.url_query = source["gen_url"][2]

    def gen_chat(self,query, gen_hist=[], ans="", generate_config={}, mode="all"):
        # gen_hist.append({
        #     "role": "user",
        #     "content": query,
        # })
        generate_config = {"temperature":"0.002"}
        body = {
            "messages": gen_hist,
            "generate_config": generate_config,
            "stream": True
        }
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
    
    def query_list(self, df, param, token):
        response = requests.post(url=self.url_query, json=param,verify = False, headers={'Content-type': 'application/json', "access-token":token})
        # print(response.text)
    
        return json.loads(response.text)

    def __call__(self, query, gen_hist):
        return self.gen_chat(query, gen_hist)

gen_model = Gen_Model()
token = gen_model.query_token()
future_list=[]
    
def test(period_i, indCode):
    df = pd.DataFrame()
    periodType = periodTypes[period_i]
    if '月' in periodType:
        periodTimeList = pd.date_range(start='2021-04', end='2024-04', freq='MS').strftime('%Y-%m')
        pT = '月'
    elif '年' in periodType:
        periodTimeList = pd.date_range(start='2021', end='2024', freq='YS').strftime('%Y')
        pT = '年'
    indexname = indexName[period_i]
    type_data = shujuxiang[period_i].replace("_v", "V")
    for zhuzhi_i, name in enumerate(zhuzhi_name):
        id = zhuzhi_id[zhuzhi_i]
        results = []
        units = []
        for periodTime in periodTimeList:
            print(periodTime)
            query_1 = {
                'indCode' :indCode ,
                'periodType':pT,
                'periodTime':periodTime,
                'orgIds': [id]
            }
            result_json = gen_model.query_list(df, query_1, token)
            if result_json.get("data", []):
                if not float(result_json['data'][0][type_data]).is_integer():
                    result = f"{float(result_json['data'][0][type_data]):.3f}"
                else:
                    result = f"{float(result_json['data'][0][type_data]):.0f}"
                # result = float(result_json['data'][0][type_data])
                unit = result_json["data"][0]["unit"]
            else:
                result = ""
                unit = ""
            results.append(result)
            units.append(unit)
        df[name] = results
        df['指标单位'] = units
        df['时间'] = periodTimeList
    df.to_csv('./data/'+indexname+'.csv', index=False)
    print('sucess')
            

            

for period_i, indCode in enumerate(indCodes):
    # if period_i > 10:
    #     break
    future = thread_pool.submit(test,period_i, indCode)
    future_list.append(future)
    

print("------------------", len(future_list))
for tmp in future_list:
    result = tmp.result()
    
print('sucess!!')