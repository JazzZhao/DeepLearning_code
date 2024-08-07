# -*- coding: utf-8 -*-
import json
from uuid import uuid1
from utils import get_feasibility_report_prompt, dfs, zhuzhi_name, zhuzhiid
from utils import tool
from utils import log_file
import logging
from concurrent.futures import ThreadPoolExecutor
import re
log_file(logging.INFO)

__all__ = ['Write_Model']

class Write_Model(object):
    def __init__(self):
        super(Write_Model, self).__init__()
        # 创建线程池
        self.thread_pool = ThreadPoolExecutor(max_workers=36)
        
    def predict(self, query,mode, section, gen_model):
        # try:
            query=re.sub(r'[\.,;:!?，。；：！？…]+$', '', query)
            third_prompt = get_feasibility_report_prompt("", query, "third")
            response_json = gen_model.gen_chat(query, third_prompt)
            third_answer = response_json["answer"].text
            third_answer_json = json.loads(third_answer)
            print("第三次生成回复："+third_answer)
            query_new = third_answer_json["陈述句"]
            first_prompt = get_feasibility_report_prompt("", query_new, "first")
            logging.info("第一次请求prompt："+json.dumps(first_prompt, ensure_ascii = False))
            # print("第一次请求prompt："+json.dumps(first_prompt, ensure_ascii = False))
            response_json = gen_model.gen_chat(query, first_prompt)
            first_answer = response_json["answer"].text
            print("第一次生成回复："+first_answer)
            first_answer_json = json.loads(first_answer)
            if not first_answer_json['category_name'] == "":
                second_prompt = get_feasibility_report_prompt(first_answer_json['category_name'], query_new, "second")
                response_json = gen_model.gen_chat(query, second_prompt)
                second_answer = response_json["answer"].text
                print("第二次生成回复："+second_answer)
                second_answer_json = json.loads(second_answer)
                if not second_answer_json['category_name'] == "":
                    second_answer_json['category_name'] = tool.find_best_match(second_answer_json['category_name'], dfs[first_answer_json['category_name']]['指标名称'].tolist())
                    print("第二次生成回复："+json.dumps(second_answer_json, ensure_ascii = False))
                    #拼接请求
                    df = dfs[first_answer_json['category_name']]
                    zbj = dfs["总表"][dfs["总表"]['指标名称']==second_answer_json['category_name']]
                    location_id = []
                    for location in third_answer_json['地点']:
                        best_match = tool.find_best_match(location, zhuzhi_name, threshold=0)
                        id_tmp = zhuzhiid[zhuzhiid['组织名称']==best_match]['人资组织ID'].values[0]
                        location_id.append(id_tmp)
                    periodType = zbj['时间'].values[0]
                    periodType,periodTimeList = tool.generate_time_list(third_answer_json['开始时间'],third_answer_json['结束时间'],periodType)
                    ans_c = {}
                    # ans_c = {
                    #     "位置":third_answer_json['地点']
                    # }
                    
                    ans_e = {
                        "location":third_answer_json['地点']
                    }
                    num = 1
                    token = gen_model.query_token()
                    zb_name = zbj["指标名称"]
                    #获取指标文件
                    zb_file = pd.read_csv("data/"+zb_name+".csv", encoding="utf-8")
                    for index in range(len(location_id)):
                        future_list = []
                        id = location_id[index]
                        location_one =  third_answer_json['地点'][index]
                        current_value = []
                        unit = ""
                        period = []
                        for periodTime in periodTimeList:
                            # query_1 = {
                            #     'indCode' : zbj['指标编码'].values[0],
                            #     'periodType':periodType,
                            #     'periodTime':periodTime,
                            #     'orgIds': [id]
                            # }
                            # future = self.thread_pool.submit(gen_model.query_list, query_1, token)
                            # future_list.append({"future":future, "periodTime":periodTime})
                            zb_file
                        
                        for tmp in future_list:
                            future = tmp["future"]
                            periodTime = tmp["periodTime"]
                            result_json = future.result()
                            result_json = json.loads(result_json.text)
                            if result_json["status"] == 200 and len(result_json["data"]) > 0:
                                unit = result_json["data"][0]["unit"]
                                period.append(periodTime)
                                type_data = zbj['数据项'].values[0].replace("_v", "V")
                                if unit == "GB":
                                    unit = "PB"
                                    result_json['data'][0][type_data] = f"{float(result_json['data'][0][type_data])/1024/1024}"
                                if not float(result_json['data'][0][type_data]).is_integer():
                                    current_value.append(f"{float(result_json['data'][0][type_data]):.3f}")
                                else:
                                    current_value.append(f"{float(result_json['data'][0][type_data]):.0f}")
                        if unit == "U154":
                            unit = "亿千瓦时"
                        ans_c["时间"] = period
                        ans_e["period"] = period
                        ans_c[location_one+second_answer_json['category_name']+"数值"] = current_value
                        ans_e["value"+str(num)] = current_value
                        ans_c["单位"] = unit
                        ans_e["unit"] = unit
                        num += 1
                    fourth_prompt = get_feasibility_report_prompt(first_answer_json['category_name'], query, "last", json.dumps(ans_c, ensure_ascii = False))
                    print(fourth_prompt)
                    response_json = gen_model.gen_chat(query, fourth_prompt, json.dumps(ans_e, ensure_ascii = False))
            print("=======最后生成的语句========")
            yield response_json
#         except Exception as err:
#             ans = "查找实时数据后，没有找到相关数据"
#             fourth_prompt = get_feasibility_report_prompt(first_answer_json['category_name'], query, "last", ans)
#             response_json = gen_model.gen_chat(query, fourth_prompt)
#             yield response_json


