from dwt_api import dwt
import prompt
import json
import pandas as pd


names = prompt.dfs['总表']['指标名称'].tolist()
category = prompt.dfs['总表']['类别'].tolist()
names_dwt = []
i=0
for name,lb in zip(names,category):
    user = '2023年11月2日广西电网'+name+'是多少'
    i=i+1
    print('---------------------------------------------------'+str(i))
    print(user)
    print('\n'+name+':'+lb)
    #分类
    yt = json.loads(dwt(prompt.get_messages1(user)))['category_name']
    print(yt)
    #指标
    zb = json.loads(dwt(prompt.get_messages2(yt,user)))['category_name']
    print(zb)
    #提取关键词
    gjc = json.loads(dwt(prompt.get_messages3(user)))
    print(gjc)
    #拼接请求
    df = prompt.dfs[yt]
    zbj = df[df['指标名称']==zb]
    query = {
        'indCode' : zbj['指标编码(需要入参给云景)'].values[0],
        'periodType':gjc['周期类型'],
        'periodTime':gjc['周期时间'],
        'orgIds': gjc['地点']
    }
    print(query)
    # names_dwt.append(zb)
df = pd.DataFrame({
    'true': names,
    'predict': names_dwt
})
df.to_excel('output2.xlsx')