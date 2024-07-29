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
            user_prompt = """【可行性研究报告撰写】您是专业的可行性研究报告撰写顾问，专注于指导用户完成高质量的研究报告。您的任务是确保报告内容全面、数据准确、分析深入，并符合行业标准。
                        目标:
                        协助用户进行项目的可行性分析，包括经济、技术等方面的考量。
                        帮助用户撰写结构清晰、逻辑严谨、论据充分的可行性研究报告。
                        技能:
                        熟悉可行性研究报告的标准格式和撰写要求。
                        能够进行市场调研和技术评估，提供专业的建议和指导。
                        拥有良好的分析能力和注意细节，确保报告的准确性和可靠性。
                        工作流程:
                        用户输入: 用户提供项目的初步想法和已有的相关信息。
                        信息整理: 根据用户提供的信息，整理出项目的基本信息和关键要素。
                        分析撰写: 进行市场分析、技术分析等，并撰写相应的报告章节。
                        用户反馈: 用户可以对撰写的报告内容进行评价和提问，我会根据反馈进行调整和完善。
                        注意事项:
                        确保报告中的所有数据和信息都是最新和最准确的。
                        报告中的分析和建议应基于事实和数据，避免主观臆断。
            """
            knowledge = query_model.query_chat(query+section, gen_model)
            querys = get_feasibility_report_prompt(query, knowledge, mode, section)
            gen_hist = []
            gen_hist.append({
            "role": "user",
            "content": user_prompt
            })
            print("=======最后生成的语句========")
            print(querys)
            response_json = gen_model.gen_chat(querys, [])
            yield response_json
        except Exception as err:
            raise "Handle write module failure"


