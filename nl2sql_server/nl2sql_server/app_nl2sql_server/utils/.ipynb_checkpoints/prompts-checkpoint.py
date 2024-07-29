# -*- coding: utf-8 -*-
import pandas as pd
from utils import tool
import datetime

today = datetime.date.today()

# dfs = pd.read_excel('./utils/大瓦特-指标列表-20240515.xlsx',sheet_name=None)
dfs = pd.read_excel('./utils/123.xlsx',sheet_name=None)

for df in dfs.values():  
    tool.clean_df(df)
df = dfs['总表']
ywy = df['类别'].drop_duplicates().tolist()
ywy = '、'.join(ywy)

zhuzhiid = pd.read_excel('./utils/人资组织id.xlsx')
tool.clean_df(zhuzhiid)
zhuzhi_name = zhuzhiid['组织名称'].tolist()


# In[] 意图识别
def get_messages1(user):
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

# In[] 指标选择
def get_messages2(lb:str,user):
    # if '南网' not in user and '南方电网' not in user:
    #     user = '南网'+user
    user=user.replace("多少", "") 
    user=user.replace("今年", today.strftime('%Y年')) 
    user=user.replace("本月", today.strftime('%Y年%m月'))
    user=user.replace("今天", today.strftime('%Y年%m月%d日'))    
    df = dfs[lb]
    if '序号' not in df.columns:
        df.insert(0, '序号', range(1, len(df) + 1)) 
    No = df['序号']
    name = df['指标名称']
    difine = df['指标定义']
    leibie = ''
    for i,name_value, define_value in zip(No, name, difine):
        if isinstance(define_value, str):
            leibie= leibie+str(i)+'.'+name_value+':'+tool.modify_string(define_value)+'。'
        else:
            leibie= leibie+str(i)+'.'+name_value+'。\n'

    # geshi ="{\"keywords\": 关键词列表,\n    \"category_name\": 类别名称,\n    \"category_number\":类别编号}\n"
    geshi ="{\"keywords\": 关键词列表,\n    \"category_name\": 类别名称\"}\n"
    system =f'''
    你是一个文本分类器，可以分析文本数据并根据用户输入分配类别，不能说不知道。
    ### 任务
    您的任务是只为输入文本分配一个类别，并且在输出中只能分配一个类别名称。此外，您需要从文本中提取与分类相关的关键词。
    ### 类别
    类别格式为："类别编号.类别名称:类别定义。"
    类别包括：{leibie}
    ### 格式
    你的回复只能以JSON的格式。
    {geshi}
    ### 注意
    你的回复只能以JSON的格式，你有实时数据但不需要提供数据，不能回复除分类之外的内容。
    你只需给文本分类，必须返回已提供的类别名称中的一个，不能说不知道！！！
    ### 开始

    '''
    if lb =='电网运维与资产管理':
        query1 = "截止目前广东电网广州供电局和广西电网南宁供电局的线损率分别有多少"
        ans1 =  "{\"keywords\": [\"截止目前\",  \"线损率\"],\n    \"category_name\": \"线损率\"}\n"
        query2 = "南方电网公司本年故障次数"
        ans2 =  "{\"keywords\": [\"南网\",  \"本年\", \"故障次数\"],\n    \"category_name\": \"本年故障次数\"}\n"
        query3 = "南方电网公司2023年输配电价"
        ans3 =  "{\"keywords\": [\"南方电网公司\", \"2023年\", \"输配电价\"],\n    \"category_name\": \"输配电价\"}\n"  
    if lb =='客户服务与市场运营':
        query1 = "截止目前服务用户数"
        ans1 =  "{\"keywords\": [\"截止目前\", \"服务用户数\"],\n    \"category_name\": \"服务用户数\"}\n"
        query2 = "今年南网报障工单数"
        ans2 =  "{\"keywords\": [\"南网\", \"报障工单数\"],\n    \"category_name\": \"报障工单数\"}\n"
        query3 = "南方电网公司2023年客户平均停电时间"
        ans3 =  "{\"keywords\": [\"南方电网公司\", \"2023年\", \"输配电价\"],\n    \"category_name\": \"客户平均停电时间\"}\n" 
    if lb =='人力资源与组织运营':
        query1 = "截止目前数字集团发明专利数"
        ans1 =  "{\"keywords\": [\"截止目前\", \"数字集团\", \"发明专利数\"],\n    \"category_name\": \"累计有效发明专利拥有数\"}\n"
        query2 = "去年本月广东电网公司干部人数"
        ans2 =  "{\"keywords\": [\"去年本月\", \"广东\", \"干部人数\"],\n    \"category_name\": \"干部人数\"}\n"   
        query3 = "南方电网公司2023年用工人数"
        ans3 =  "{\"keywords\": [\"南方电网公司\", \"2023年\", \"用工人数\"],\n    \"category_name\": \"用工人数\"}\n"  
    if lb =='环境保护与能源管理':
        query1 = "今年广西电网的绿色交易用户数有多少"
        ans1 =  "{\"keywords\": [\"今年\", \"绿色交易用户数\"],\n    \"category_name\": \"绿色交易用户数\"}\n"
        query2 = "去年全年广东省广州市供电量"
        ans2 =  "{\"keywords\": [\"去年\", \"广西\", \"供电量\"],\n    \"category_name\": \"供电量\"}\n"  
        query3 = "南方电网公司2023年供电量"
        ans3 =  "{\"keywords\": [\"南方电网公司\", \"2023年\", \"供电量\"],\n    \"category_name\": \"供电量\"}\n"            
    if lb =='财务和投资管理':
        query1 = "今年南网广东电网广州供电局净利润"
        ans1 =  "{\"keywords\": [\"今年\", \"南网\", \"净利润\"],\n    \"category_name\": \"净利润\"}\n"
        query2 = "去年海南省三亚市售电平均单价"
        ans2 =  "{\"keywords\": [\"去年\", \"海南\", \"售电平均单价\"],\n    \"category_name\": \"售电平均单价\"}\n"    
        query3 = "南方电网公司2023年输配电价"
        ans3 =  "{\"keywords\": [\"南方电网公司\", \"2023年\", \"输配电价\"],\n    \"category_name\": \"输配电价\"}\n"  

    messages_zb = [
                {"role":"user", "content":system+query1},
                {"role":"assistant", "content":ans1},
                {"role":"user", "content":query2},
                {"role":"assistant", "content":ans2},
                {"role":"user", "content":query3},
                {"role":"assistant", "content":ans3},
                {"role":"user", "content":user}]
    return messages_zb
# In[] 关键词提取
def get_messages3(user):
    user=user.replace("多少", "") 
    user=user.replace("五省", "广东、广西、贵州、海南、云南") 
    system =f'''
    你是一个关键词提取器，可以分析任何文本内容并根据用户输入提取关键词，不能说不知道。
    ### 任务
    您的任务是为输入文本提取开始时间、结束时间、地点和陈述句等4个关键词，并且以JSON格式返回。
    ### 关键词
    关键词有三个：开始时间、结束时间、地点。
    开始时间：提取输入中的时间段开始，格式为"%Y-%m-%d"。例如输入2023年1月到3月，输出20230101；输入2013年5月14日，输出2013-05-14。如未提及时间默认为今天。
    结束时间：提取输入中的时间段开始，格式为"%Y-%m-%d"。例如输入2023年1月到3月，输出20230331；输入2013年5月14日，输出2013-05-14。如未提及时间默认为今天。
    地点：提取输入中的地点。分成三级。由上到下为网级、省级、市级。网级只包含南方电网；省级为南网五省包含广东、广西、云南、贵州、海南等5个；市级包含南网五省各地级市，如广州、佛山、桂林等。多个地点以列表形式输出，多级地点输入以最低级别地点为最终输出,例如广东省广州市和海南三亚得输出为[广州,三亚]，如果没有提到地点默认为[南方电网]。
    陈述句：把用户输入剔除时间与地点等信息后，变成新的陈述句。
    ### 注意
    今天是{today.strftime('%Y年%m月%d日')}。
    你只需要提取开始时间、结束时间和地点等3个关键词，不能说不知道！！！
    你的回复只能以JSON的格式，不能回复除关键词之外的内容。
    ### 开始

    '''
    query1 = "去年上半年南网充电枪总共收了多少电费"
    ans1 =  "{\"开始时间\": \"2023-01-01\", \n    \"结束时间\": \"2023-06-30\", \n    \"地点\": [\"南网\"], \n    \"陈述句\": \"充电枪收电费\"}\n"
    query2 = "近三年交流充电桩有多少"
    ans2 =   "{\"开始时间\": \"2021-01-01\", \n    \"结束时间\": \"2024-12-31\", \n    \"地点\": [\"南方电网\"], \n    \"陈述句\": \"交流充电桩\"}\n"
    query3 = "今天广东省广州供电局和深圳供电局负荷是多少"
    ans3 =   f"{{\"开始时间\": \"{today.strftime('%Y-%m-%d')}\", \n    \"结束时间\": \"{today.strftime('%Y-%m-%d')}\", \n    \"陈述句\": \"负荷\"}}\n"
    query4 = "请告诉我今年1月到4月广西南宁和海南三亚的供电量"
    ans4 =   "{\"开始时间\": \"2024-01-01\", \n    \"结束时间\": \"2024-04-30\", \n    \"地点\": [\"南宁\",\"三亚\"], \n    \"陈述句\": \"供电量\"}\n"
    query5 = "2024年一季度广州和佛山负荷分别是多少"
    ans5 =   "{\"开始时间\": \"2024-01-01\", \n    \"结束时间\": \"2024-03-31\", \n    \"地点\": [\"广州\",\"佛山\"], \n    \"陈述句\": \"负荷\"}\n"
    query6 = "截止目前广东省广州市电力营业厅个数"
    ans6 =   f"{{\"开始时间\": \"{today.strftime('%Y-%m-%d')}\", \n    \"结束时间\": \"{today.strftime('%Y-%m-%d')}\", \n    \"地点\": [\"广州\"], \n    \"陈述句\": \"电力营业厅个数\"}}\n"

    messages_gjc = [
                {"role":"user", "content":system+query1},
                {"role":"assistant", "content":ans1},
                {"role":"user", "content":query2},
                {"role":"assistant", "content":ans2},
                {"role":"user", "content":query3},
                {"role":"assistant", "content":ans3},
                {"role":"user", "content":query4},
                {"role":"assistant", "content":ans4},
                {"role":"user", "content":query5},
                {"role":"assistant", "content":ans5},
                {"role":"user", "content":query6},
                {"role":"assistant", "content":ans6},
                {"role":"user", "content":user}]
    return messages_gjc

# In[] 回复用户
def get_messages4(user,ans):
    messages=[{"role":"user", "content":"你是问答机器人\“大瓦特\”。\n用户问题："+user+'？'+"\n查询得到数据是："+str(ans)+"\n请回复用户问题："}]
    return messages

# 获取周报prompt
def get_feasibility_report_prompt(label, query, mode="all", ans="", section = ""):
    
    if mode == "third":
        return get_messages3(query)
    elif mode == "second":
        return get_messages2(label, query)
    elif mode == "first":
        return get_messages1(query)
    elif mode == "last":
        return get_messages4(query,ans)
    # elif stage == "0_1":
    #     return second_feasibility_report_prompt.format(query)
    # if stage == "0_2":
    #     return third_feasibility_report_prompt.format(query)
    else:
        raise NotImplementedError