import datetime
import Levenshtein as lev
import calendar
import pandas as pd
import re


def modify_string(s):
    # 检查字符串是否为空
    if not s:
        return s
    
    # 定义标点符号的正则表达式
    punctuation_pattern = r"[，。！？、；：,.!?;:]"
    
    # 获取最后一个字符
    last_char = s[-1]
    # 判断最后一个字符是否为标点符号
    if re.search(punctuation_pattern, last_char):
        # 如果是标点符号，则替换为'？'
        return s[:-1]
    else:
        # 如果不是标点符号，加上'？'
        return s
    
# 清除列名中的制表符和前后空格
def clean_df(df):
    df.columns = df.columns.str.replace('\t', '').str.strip()
    for column in df.columns:
        if df[column].dtype == 'object':  # 仅对字符串类型的列进行处理
            df[column] = df[column].str.replace('\t', '').str.strip()
            
def find_best_match(target, strings, threshold=0.6):
    best_match = None
    min_distance = float('inf')
    
    for s in strings:
        dist = lev.distance(target, s)
        lev_ratio = 1 - dist / max(len(target), len(s))
        if dist < min_distance:
            min_distance = dist
            best_ratio = lev_ratio
            best_match = s
    if best_ratio>threshold:
        return best_match
    else:
        raise ValueError("不匹配")

def generate_time_list(start_date,end_date, allowed_units):
    # Determine the level of granularity in input time
    # date_parts = input_time.count('-')
    today = datetime.date.today()
    end_date = end_date if datetime.datetime.strptime(end_date, '%Y-%m-%d').date() < today else today.strftime('%Y-%m-%d')
    # Create a date range based on input time and allowed units
    # if date_parts == 0:  # Yearly granularity
    #     start_date = f"{input_time}-01-01"
    #     end_date = f"{input_time}-12-31"
    #     end_date = end_date if datetime.datetime.strptime(end_date, '%Y-%m-%d').date() < today else today.strftime('%Y-%m-%d')
    #     if '年' in allowed_units:
    #         return '年',[input_time]
    #     if '月' in allowed_units:
    #         return '月',pd.date_range(start=start_date, end=end_date, freq='M').strftime('%Y-%m')
    #     if '日' in allowed_units:
    #         return '日',pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y-%m-%d')
    
    # elif date_parts == 1:  # Monthly granularity
    #     start_date = f"{input_time}-01"
    #     end_date = pd.to_datetime(start_date).to_period('M').end_time.strftime('%Y-%m-%d')
    #     end_date = end_date if datetime.datetime.strptime(end_date, '%Y-%m-%d').date() < today else today.strftime('%Y-%m-%d')
    #     if '月' in allowed_units:
    #         return '月',[input_time]
    #     if '年' in allowed_units:
    #         return '年',[input_time[:4]]
    #     return '日',pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y-%m-%d')
    # else:  # Daily granularity
    if '日' in allowed_units:
        return '日',pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y-%m-%d')
    if '月' in allowed_units:
        return '月',pd.date_range(start=start_date[:7], end=end_date[:7], freq='MS').strftime('%Y-%m')
    if '年' in allowed_units:
        return '年',pd.date_range(start=start_date[:4], end=end_date[:4], freq='YS').strftime('%Y')
    # Generate date range

# # Example usage with the preference to show only months for "2024" with allowed "月、日"
# generate_time_list_final("2024", "月、日")

# 测试函数
# print(generate_time_list("2024", "日"))   
# print(generate_time_list("2024-01-01", "月"))   
# print(generate_time_list("2023-11", "日"))     
