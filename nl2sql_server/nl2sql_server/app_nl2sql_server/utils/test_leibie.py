from dwt_api import dwt
import json
import pandas as pd
import tool
import re
import datetime

today = datetime.date.today()

def get_messages1(ywy, user):
    user=user.replace("多少", "") 
    user=user.replace("今年", today.strftime('%Y年')) 
    user=user.replace("本月", today.strftime('%Y年%m月'))
    user=user.replace("今天", today.strftime('%Y年%m月%d日'))
    system =f'''
    你是一个文本分类器，可以分析文本数据并根据用户输入分配类别，不能说不知道。
    ### 任务
    您的任务是只为输入文本分配一个类别，并且在输出中只能分配一个类别名称。此外，您需要从文本中提取与分类相关的关键词。
    ### 类别
    类别包括：{ywy}
    ### 注意
    你的回复只能以JSON的格式，你有实时数据但不需要提供数据，不能回复除分类之外的内容。
    你只需给文本分类，必须回答不能说不知道！！！
    ### 开始吧！

    '''
    query1 = "2023年11月3日广东绿色交易电量是多少"
    ans1 =  "{\"keywords\": [\"广东\", \"绿色交易电量\", \"2023年11月3日\"],\n    \"category_name\": \"环境保护与能源管理\"}\n"
    query2 = "2022年1季度深圳供电局的停电时长"
    ans2 =  "{\"keywords\": [\"2022年\", \"深圳供电局\", \"停电时长\"],\n    \"category_name\": \"故障停电能量\"}\n"
    query3 = "2023年12月广州交流充电枪有多少"
    ans3 =  "{\"keywords\": [\"广州\", \"交流\", \"充电枪\", \"有多少\"],\n    \"category_name\": \"充电桩设备终端\"}\n"
    query4 = "2023年海南有多少电力用户"
    ans4 =  "{\"keywords\": [\"2023年\", \"海南\", \"电力用户\", \"有多少\"],\n    \"category_name\": \"人资企业管理\"}\n"
    query5 = "2023年交流充电枪总数是多少"
    ans5 =  "{\"keywords\": [\"2023年\", \"交流充电枪\", \"总数\"],\n    \"category_name\": \"充电桩设备终端\"}\n"
    messages_yt = [
                {"role":"user", "content":system+query1},
                {"role":"assistant", "content":ans1},
                # {"role":"user", "content":query2},
                # {"role":"assistant", "content":ans2},
                # {"role":"user", "content":query3},
                # {"role":"assistant", "content":ans3},
                # {"role":"user", "content":query4},
                # {"role":"assistant", "content":ans4},
                # {"role":"user", "content":query5},
                # {"role":"assistant", "content":ans5},
                {"role":"user", "content":user}]
    return messages_yt
# pd.da
# In[] 未定义类别指标，给出类别
# dfs = pd.read_excel('D:/code/yunjing/指标 - 云景正式库.xls',sheet_name=None)
# df = dfs['Sheet4']
# names = df['指标名称'].tolist()
names = ["调度统调当日受电量",
"调度统调当日水电发电量",
"调度统调当日气电发电量",
"调度统调当日煤电发电量",
"调度统调当日火电发电量",
"调度统调当日光伏发电量",
"调度统调当日风电发电量",
"调度统调当日发受电量",
"调度统调当日发电量"
]
ywy='财务和投资管理、客户服务与市场运营、电网运维与资产管理、环境保护与能源管理、人力资源与组织运营'
yt_dwt = []
i=0
for name in names:  
    user = '今年一季度南方电网公司'+name+'是多少'
    user = re.sub(r'[\.,;:!?，。；：！？…]+$', '', user)
    i=i+1
    print('---------------------------------------------------'+str(i))
    print(name)
    yt = json.loads(dwt(get_messages1(ywy,user)))['category_name']
    print(yt)
    # yt_dwt.append(yt)
    # #提取关键词
    # print(prompt.get_messages3(user))
    # gjc = json.loads(dwt(prompt.get_messages3(user)))
    # print(gjc)
    # new_user = gjc['陈述句']
    # #分类
    # response1 = dwt(prompt.get_messages1(ywy,new_user))
    # # try:
    # yt = json.loads(response1)['category_name']

# df['类别'] = yt_dwt
# df.to_excel('D:/code/yunjing/大瓦特-指标列表-20240517-1.xlsx')
# dfs={'总表':df}
# for lb in ['财务和投资管理','客户服务与市场运营','电网运维与资产管理','环境保护与能源管理','人力资源与组织运营']:
#     dfs[lb] = df[df['类别']==lb]
# with pd.ExcelWriter('D:/code/yunjing/大瓦特-指标列表-20240520-新增.xlsx') as writer:  
#     for sheet_name, df in dfs.items():  
#         # 将每个 DataFrame 写入到对应的 sheet 中  
#         df.to_excel(writer, sheet_name=sheet_name, index=False)












# In[] 把分错类别的指标，加入子sheet
# dfs = pd.read_excel('D:/code/yunjing/123.xlsx',sheet_name=None)
# for df in dfs.values():  
#     tool.clean_df(df)
# df = dfs['总表']

# names = df['指标名称'].tolist()
# category = df['类别'].tolist()
# ywy = df['类别'].drop_duplicates().tolist()
# ywy = '、'.join(ywy)
# yt_dwt = []
# name_dwt = []
# error = []
# i=0

# for name,lb in zip(names,category):
#     user = '广州、深圳和佛山2022年下半年'+name+'是多少'
#     i=i+1
#     print('---------------------------------------------------'+str(i))
#     print(user)
#     print('\n'+name+':'+lb)
#     try:
#     #分类
#         yt = json.loads(dwt(prompt.get_messages1(ywy,user)))['category_name']
#         print(yt)
#         if yt != lb:
#             yt_dwt.append(yt)
#             name_dwt.append(name)
#             if name not in dfs[yt]['指标名称'].tolist():
#                 dfs[yt] = pd.concat([dfs[yt], df[df['指标名称']==name]], ignore_index=True)
#             print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            
#     except:
#         error.append(name)
#         print('bbbbb')
# with pd.ExcelWriter('D:/code/yunjing/123456.xlsx') as writer:  
#     for sheet_name, df in dfs.items():  
#         # 将每个 DataFrame 写入到对应的 sheet 中  
#         df.to_excel(writer, sheet_name=sheet_name, index=False)