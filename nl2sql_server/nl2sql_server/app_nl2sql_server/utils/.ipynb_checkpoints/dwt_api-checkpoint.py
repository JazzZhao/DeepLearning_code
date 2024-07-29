# In[] 意图识别
import hashlib
import time
import requests
import prompt
import json
import tool
import pandas as pd
# APPSECRET = 'e7d86783584a4295a6604081e8cbad35'
# APPID = 'gaixcwatt-virtually'
# url = "https://ai.csg.cn/virtually/llm/model/predict"

APPID="gaixc-security"
APPSECRET="255050d75950490e9f23a37f9c87a6cd"

url = "https://ai.csg.cn/security/llm/model/predict"
def dwt(messages):
    timestamp = int(time.time() * 1000)
    keystr = APPID + "UZ" + APPSECRET + "UZ" + str(timestamp)
    localappkey = hashlib.sha256(keystr.encode()).hexdigest()
    APPKEY = localappkey + '.' + str(timestamp)
    url = "https://ai.csg.cn/virtually/llm/model/predict"

    params = {"messages":messages, "generate_config":{"temperature":"0.002"}}
    headers = {"Content-Type":"application/json",
            "Referer":"https://ai.csg.cn/",
            "APP-KEY":APPKEY,
            "APP-ID":APPID}

    response=requests.post(url=url,
                        json=params,
                        stream=True,
                        headers=headers,
                        cert=False)
    final_result = ''
    for chunk in response.iter_content(1024):
        print(chunk.decode("utf-8", "ignore"), end="")
        final_result += chunk.decode("utf-8", "ignore")
    return final_result

if __name__ =='__main__':
    #读取指标表
    dfs = pd.read_excel('D:/code/yunjing/123.xlsx',sheet_name=None)
    for df in dfs.values():  
        tool.clean_df(df)
    df = dfs['总表']
    ywy = df['类别'].drop_duplicates().tolist()
    ywy = '、'.join(ywy)
    #读取组织表
    zhuzhiid = pd.read_excel('D:/code/yunjing/人资组织id.xlsx')
    tool.clean_df(zhuzhiid)
    zhuzhi_name = zhuzhiid['组织名称'].tolist()

    user = "2024年一季度广东广州和广西的输配电价格哪个高"
    #分类
    response1 = dwt(prompt.get_messages1(ywy,user))
    # try:
    yt = json.loads(response1)['category_name']

    print(yt)
    #指标
    print(prompt.get_messages2(yt,dfs,user))
    zb = json.loads(dwt(prompt.get_messages2(yt,dfs,user)))['category_name']
    zb = tool.find_best_match(zb,dfs[yt]['指标名称'].tolist())
    print(zb)
    #提取关键词
    # print(prompt.get_messages3(user))
    gjc = json.loads(dwt(prompt.get_messages3(user)))
    print(gjc)
    #拼接请求
    zbj = df[df['指标名称']==zb]
    location_id = []
    for location in gjc['地点']:
        best_match = tool.find_best_match(location, zhuzhi_name)
        id = zhuzhiid[zhuzhiid['组织名称']==best_match]['人资组织ID'].values[0]
        location_id.append(id)
    periodType = zbj['时间'].values[0]
    periodType,periodTimeList = tool.generate_time_list(gjc['开始时间'],gjc['结束时间'],periodType)

    for id in location_id:
        for periodTime in periodTimeList:
            query = {
                'indCode' : zbj['指标编码'].values[0],
                'periodType':periodType,
                'periodTime':periodTime,
                'orgIds': id
            }
            print(query)

    ans = '''
{"msg":"广州","data":[{ "date":"2024-01", "value":"0.9"},
{"date":"2024-02", "value":"0.93"},
{"date":"2024-03", "value":"0.96" },
{"date":"2024-04", "value":"0.91"},] }
{"msg":"广西","data":[{ "date":"2024-01", "value":"0.9"},
{"date":"2024-02", "value":"0.93"},
{"date":"2024-03", "value":"0.96" },
{"date":"2024-04", "value":"0.91"},] }'''

    response = dwt(prompt.get_messages4(user,ans))
    print(response)
    # except:
    #     ans = "查找实时数据后，没有找到相关数据"
    #     response = dwt(prompt.get_messages4(user,ans))
