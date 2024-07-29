# -*- coding: utf-8 -*-
import warnings
import json
import requests
import random
import logging
import get_logger

get_logger.log_file(logging.INFO)

warnings.filterwarnings("ignore")

class Gen_Model():

    def __init__(self):
        with open("config.json", encoding="utf-8") as req_source:
            source = json.loads(req_source.read())
            self.url = source["gen_url"][0]

    def gen_chat(self, query, gen_hist=[], generate_config={}, mode="all"):
        gen_hist.append({
            "role": "user",
            "content": query,
        })
        body = {
            "messages": gen_hist,
            "generate_config": generate_config,
            "stream": True
        }
        proxies = {'http': None, 'https': None}
        response = requests.post(url=self.url, json=body, stream=True, headers={'Content-type': 'application/json'}, proxies=proxies)
        response_json = {}
        response_json["query"] = query
        response_json["answer"] = response
        return response_json

    def __call__(self, query, gen_hist):
        return self.gen_chat(query, gen_hist)

class Query_Model():

    def __init__(self):
        with open("config.json", encoding="utf-8") as req_source:
            source = json.loads(req_source.read())
            self.url = source["query_url"][0]

    def query_chat(self, query,gen_model, model=1):
        payload=json.dumps({
            "query":query,
            "csid":"123456",
            "topn":5,
            "threshold":0.75
        })
        headers = {
            'Content-Type':'application/json'
        }
        if model == 1:
            answers = ""
        elif model == 2:
            answers = []
        proxies = {'http': None, 'https': None}
        response=requests.request("POST",self.url, headers=headers,data=payload, proxies=proxies)
        if response.status_code == 200:  
            # 解析JSON响应
            try:
                data = json.loads(response.text)
                # 检查errorcode是否是200
                if data['errorcode'] == '200':  
                    # 遍历result列表，获取每个answer字段  
                    for item in data['data']['result']:
                        logging.info("匹配的query:"+item['query'] + '\n')
                        logging.info("匹配的answer:"+item['answer'] + '\n')
                        if model == 1:
                            answers += item['answer']
                        elif model == 2:
                            answers.append(item['answer'])
                else:  
                    logging.info(f"Error occurred with errorcode: {data['errorcode']}. Message: {data['message']}")  
            except Exception as e:  
                logging.error(f"JSON decoding error: {e}") 
        else:
            logging.info(f"Error occurred with status code: {response.status_code}")
        if model == 1:
            return answers
        else:
            return compress_answer(answers, 1500, query, gen_model)

    def __call__(self, query, gen_hist):
        return self.gen_chat(query, gen_hist)

def compress_answer(answers, max_len, query, gen_model):
    tmp = ""
    result = ""
    # compress_prompt = "你现在的任务是帮助我找到关键内容，你从材料中找到和\"深度学习中的大模型时代，自然语言处理的技术突破点\"相关的内容，我给你的材料是：\n\"{}\"。你生成的是：\n"
    compress_prompt = """目的：从长文本中提取与[{}]相关的关键信息，保证信息完整。
                步骤：
                理解主题：首先，确保对[{}]有清晰的理解。
                文本预览：快速浏览整个文本。
                关键词识别：根据[{}]，列出相关的关键词和短语，这些将在文本搜索中作为指引。
                搜索与定位：使用文本搜索工具或功能（如Ctrl+F或Command+F），输入关键词，快速定位文本中与[{}]相关的段落或句子。
                上下文分析：对于搜索结果，不仅要关注关键词本身，还要阅读其上下文，以充分理解信息的含义和重要性。
                信息摘录：对于找到的相关内容，进行摘录或总结，确保记录下所有与[{}]直接相关的信息。
                信息整理：将摘录的信息进行整理，归纳出主要观点、支持细节和可能的结论。
                复查验证：复查整理后的信息，确保其准确性和与[{}]的相关性。如有疑问，返回原文进行核实。
                注意事项：
                确保分析过程中保持客观和中立，避免主观臆断。
                保持对文本的尊重，不篡改或断章取义。
                在分析过程中，如遇到难以理解或专业性较强的内容，可寻求专业人士的帮助。
                长文本内容：
                [{}]
    """
    if len(answers) < 3:
        tmp = "\n".join(answers)
        return tmp
    for answer in answers:
        if len(tmp+answer) > max_len:
            print("====压缩前=====")
            print(tmp)
            response_json = gen_model.gen_chat(compress_prompt.format(query,query,query,query,query,query,tmp), [])
            compress_answer = response_json["answer"].text
            print("====压缩后=====")
            print(compress_answer)
            result += compress_answer+ "\n"
            tmp = answer +"\n"
        else:
            tmp += answer+"\n"
    if not tmp == "":
        print("====压缩前=====")
        print(tmp)
        response_json = gen_model.gen_chat(compress_prompt.format(query,query,query,query,query,query,tmp), [])
        compress_answer = response_json["answer"].text
        print("====压缩后=====")
        print(compress_answer)
        result += compress_answer+ "\n"
    return result


if __name__ == "__main__":
    gen_model = Gen_Model()
    query_model = Query_Model()
    # first_feasibility_report_prompt = """你现在的任务是帮助我构造问答对，我给你问题的答案，你根据答案来生成相关的问题，使得该问题能够被我提供的答案很好的回答，生成的问题要求精炼，能够突出>重点，我给你的答案是：\n\"{}\"。你生成的问题是：\n
    # """
    # first_feasibility_report_prompt = "你现在的任务是帮助我找到关键内容，我给你材料，你根据材料来生成一条简短的句子，生成的句子要求尽可能多的将关键内容找出来，能够突出>重点，，我给你的材料是：\n\"{}\"。你生成的是：\n"
    # query = """你现在的任务是根据材料找出几个关键词，生成内容必须是专业词语，以逗号分隔，我给你的材料是：\n\"{}\"。你生成的是：\n"""
    # query = """根据材料进行扩展，生成内容必须和材料相关，生成内容必须是专业词语，以逗号分隔，我给你的材料是：\n\"{}\"。你生成的是：\n"""
    # 判断用户要求生成的哪部分
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
    # all_feasibility_report_prompt = """你现在是一名专业的科技项目可行性研究报告写作者，擅长参考材料，围绕主题生成专业的文字， 
    #         主题如下：\n\"{}\"，主题到此结束。 \n
    #         要求如下；\n\"{}\"，要求到此结束。 \n
    #         参考材料如下：\n\"{}\"，参考材料到此结束。\n
    #         注：生成内容不能直接引用参考材料！生成内容必须进行二次创作！
    # """
    # all_feasibility_report_prompt = """你现在是一名专业的科技项目可行性研究报告写作者，擅长参考材料，围绕主题生成专业的文字
    #         主题如下：\n\"{}\"，主题到此结束。 \n
    #         参考材料如下：\n\"{}\"，参考材料到此结束。\n
    #         注：生成内容不能直接引用参考材料！生成内容必须进行二次创作！
    # """
    all_feasibility_report_prompt = """
            写作任务如下：\n\"{}\"，写作任务到此结束。 \n
            参考材料如下：\n\"{}\"，参考材料到此结束。\n
            注意：生成内容不能直接引用参考材料！生成内容必须进行二次创作！
    """
    gen_hist = []
    gen_hist.append({
            "role": "user",
            "content": user_prompt
        })
    # gen_model.gen_chat(all_feasibility_report_prompt.format("输配电行业中大模型知识库的技术突破点", "请明确指出项目计划在哪些技术领域实现突破，包括希望达到的关键技术指标。同时，描述公司当前的技术能力，以及项目完成后预期达到的技术水准。请在500字以内提供这些信息。",""), gen_hist)
    query = "深度学习中的大模型时代，自然语言处理的问题"
    # query = "基于分组混合并行训练的方法"
    knowledge = query_model.query_chat(query, 1)   
    print("================"+knowledge+"===============")
    response_json = gen_model.gen_chat(all_feasibility_report_prompt.format(query,knowledge), [])
    print(response_json["answer"].text)
    # query_model = Query_Model()
    # query_model.query_chat("写一篇新能源报告")