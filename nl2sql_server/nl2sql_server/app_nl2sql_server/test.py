import pandas as pd
import requests

# dfs = pd.read_excel("./utils/123.xlsx",sheet_name=None)
# def clean_df(df):
#     df.columns = df.columns.str.replace('\t', '').str.strip()
#     for column in df.columns:
#         if df[column].dtype == 'object':  # 仅对字符串类型的列进行处理
#             df[column] = df[column].str.replace('\t', '').str.strip()

# for df in dfs.values():
#     clean_df(df)
# df = dfs["总表"]

# for tmp in df['指标名称']:
#     param = {
#         "query":"2023年一季度广东的"+tmp+"是多少"
#     }
#     response = requests.post(url="http://192.168.210.240:63000/nl2sql", json=param, headers={"Content-type":"application/json"})

# zb_file = pd.read_csv("./utils/data/调度当日新能源发电量.csv", encoding="utf-8")
# print(zb_file["时间"])

param = {
    # "query":"2023年一季度广东"+'负荷'+"是多少"
    "query":'广东电网2023年新能源占比'
}
response = requests.post(url="http://192.168.77.8:63000/nl2sql", json=param, headers={"Content-type":"application/json"})
print(response.text)