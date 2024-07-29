# -*- coding: utf-8 -*-
import json
from uuid import uuid1
from prompts import get_feasibility_report_prompt


__all__ = ['Write_Model']

class Write_Model(object):
    def __init__(self):

        super(Write_Model, self).__init__()
        
        # with open("config.json", encoding="utf-8") as req_source:
        #     source = json.loads(req_source.read())
        #     # 报告写作prompt
        #     self.feasibility_studies_written_config = source["feasibility_studies_written_config"]

    def predict(self, query,mode, section, gen_model, query_model):
        try:
            # 报告生成
            # 占位符
            # placeholders = self.feasibility_studies_written_config["template_style"]['0']["placeholders"]
            # 根据占位符分段生成
            # for placeholder_index, placeholder in enumerate(placeholders):
            #     stage = "0" + "_" + str(placeholder_index)  # 模板id+占位符
            #     if placeholder in ["一、目的和意义"]:
            #         querys = get_feasibility_report_prompt(query, stage=stage)
            #     elif placeholder in ["二、项目研究的背景"]:
            #         querys = get_feasibility_report_prompt(query, stage=stage)
            #     else:
            #         querys = get_feasibility_report_prompt(query, stage=stage)
                
            #     if not isinstance(querys, list):
            #         querys = [querys]

            #     for i, query_prompt in enumerate(querys):
            #         while True:
            #             try:
            #                 response_json = gen_model.gen_chat(query_prompt, [])
            #                 if (response_json["answer"].text.count("课题（任务）") 
            #                     + response_json["answer"].text.count("课题研究（任务）")
            #                     + response_json["answer"].text.count("课题(任务)")
            #                     + response_json["answer"].text.count("课题研究(任务)")  
            #                     + response_json["answer"].text.count("课题：") >= 5
            #                     or not placeholder_index==2):
            #                     break
            #             except Exception as e:
            #                 print(e)
            #                 raise "Handle write module failure"
            #         name = "公司科技项目可研报告"
            #         response_json["query"] = name
            #         response_json["placeholder_name"] = placeholder
            #         # 组成文件名的唯一标识
            #         str_now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            #         uuid = str(uuid1()).replace('-', '')
            #         response_json["file_name"] = "可研报告_{}_{}_{}.docx".format(name,str_now_time,uuid)
            #         yield response_json
            knowledge = query_model.query_chat(query+section)
            querys = get_feasibility_report_prompt(query, knowledge, mode, section)
            response_json = gen_model.gen_chat(querys, [])
            yield response_json
        except Exception as err:
            raise "Handle write module failure"


