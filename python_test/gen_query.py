# -*- coding: utf-8 -*-
import warnings
import json
import requests
import random

warnings.filterwarnings("ignore")

class Gen_Model():

    def __init__(self):
        with open("config.json", encoding="utf-8") as req_source:
            source = json.loads(req_source.read())
            self.url = source["gen_url"][0]

    def gen_chat(self, query, gen_hist=[], generation_config={}, mode="all"):
        gen_hist.append({
            "role": "user",
            "content": query
        })
        body = {
            "messages": gen_hist,
            "generation_config": generation_config,
            "stream": True
        }
        proxies = {'http': None, 'https': None}
        response = requests.post(url=self.url, json=body, stream=True, headers={'Content-type': 'application/json'}, proxies=proxies)
        response_json = {}
        response_json["query"] = query
        response_json["answer"] = response
        print(response.text)
        return response_json

    def __call__(self, query, gen_hist):
        return self.gen_chat(query, gen_hist)

class Query_Model():

    def __init__(self):
        with open("config.json", encoding="utf-8") as req_source:
            source = json.loads(req_source.read())
            self.url = source["query_url"][0]

    def query_chat(self, query):
        payload=json.dumps({
            "query":query,
            "csid":"123456",
            "topn":5
        })
        headers = {
            'Content-Type':'application/json'
        }
        answer = ""
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
                        print(item['answer'] + '\n')
                        answer += item['answer']
                else:  
                    print(f"Error occurred with errorcode: {data['errorcode']}. Message: {data['message']}")  
            except Exception as e:  
                print(f"JSON decoding error: {e}") 
        else:
            print(f"Error occurred with status code: {response.status_code}")
        return answer

    def __call__(self, query, gen_hist):
        return self.gen_chat(query, gen_hist)

if __name__ == "__main__":
    gen_model = Gen_Model()
    # first_feasibility_report_prompt = """你现在的任务是帮助我构造问答对，我给你问题的答案，你根据答案来生成相关的问题，使得该问题能够被我提供的答案很好的回答，生成的问题要求精炼，能够突出>重点，我给你的答案是：\n\"{}\"。你生成的问题是：\n
    # """

    # first_feasibility_report_prompt = """你现在的任务是帮助我找到关键内容，我给你材料，你根据材料来生成一条简短的句子，生成的句子要求尽可能多的将关键内容找出来，能够突出>重点，，我给你的材料是：\n\"{}\"。你生成的是：\n
    # """
    # query1 = """锂离子电池SOC估算方法的多样性和最新研究进展，旨在为读者提供深入理解和研究视角。"""
    # query2 = """锂离子电池安全性受关注，因极端条件和误用易引发事故，研究涉及爆炸原因和机制。"""
    # query3 = """电池性能与使用寿命受多种因素影响，包括充放电过程、环境条件等；深入研究有助于锂离子电池的开发和应用。"""
    # query4 = """硫正极材料在高能量密度锂电池中具有重要地位，但仍有导电性和安全问题亟待解决。"""
    # query5 = """钾离子电池研究关注低成本储能，面临离子半径大和电极材料选择的挑战。"""
    # query6 = """钠离子电池的研究聚焦于高性能储钠电极材料，以低成本和高资源量的优势替代锂离子电池，其中TNO类化合物因其良好的钠储存性能而受到关注，相关研究在材料结 构、应用成果和改良方向上取得进展。"""

    # query = "综述了锂离子电池荷电状态（SOC）的不同估算方法，希望能够结合作者在该领域的经验为读者提供一些见解和研究视角。电池管理系统 （BMS） 需要不断更新电池 SOC 的估计值，用于计算修正电池健康状态、能量状态以及功率状态（功能状态），并防止电池出现过充或者过放情况。已许多方法用于估计电池的 SOC，其中有些方法更具优势。该文解说了电池 SOC 的物理含义，有助区分真实 SOC 以及工程 SOC 的估算方法；对于不同的估计方法进行了较为详细的讨论；并介绍了池包 SOC 指标的定义问题以及电池包中每个单体电池的 SOC 计算方法；最后，评述了目前该领域研究前沿，并展望了未来需要开展的工作。"
    # query = "随着锂离子电池的不断推广，锂离子电池的安全性越来越受到关注。 由于工作条件以及工作环境等的原因，锂离子电池可能工作在一些极端条件如高温、低温下；或者未按规定使用电池，使其工作在过充、过放、短路、冲击等极端条件下，这些可能导致电池发生意外如着火或者爆炸等。 从导致锂离子电池爆炸的原因着手，分类综述研究了锂离子电池致爆机理和爆炸时间。"
    # query = "电动车辆的性能和成本很大程度上取决于动力电池组的性能和使用寿命，而电池组的性能和使用寿命又受到电池单体产热的影响．研究锂离子电池充放电过程中的产热特性及影响因素，对锂电池的开发及使用具有指导意义。本文从环境温度、充放电倍率、电池材料、荷电状态和老化程度五个方面入手，综述了各因素对锂离子电池产热的影响．"
    # query = "硫正极材料具有比容量高、资源丰富、环境友好等特点，由它与锂金属负极组成锂硫电池是一种极具应用前景的高能量密度的电池体系，在市场上有着极大的发展空间。硫基正极材料作为锂硫电池的重要组成部分，是提高电池性能的关键之一，也是目前的研究重点。然而锂硫电池还存在着一些比较严重的问题，如硫的导电性差、“穿梭效应”和锂晶枝等。本文综述了近几年国内外锂硫电池硫正极材料在单质硫、金属硫化物和有机硫化物三个方面的最新研究进展，并展望了锂硫电池硫正极材料的发展方向。"
    # query = "锂离子电池（LIBS）已经广泛应用到便携式电子产品和电动汽车上.  然而，随着锂资源的开采使用，锂离子电池的成本也在逐渐增加.  相比之下，地壳中较高的钾含量使得钾离子电池（KIB）成本相对较低.  进而，钾离子电池作为一种新型低成本储能器件受到了广泛关注.  但钾离子的半径较大，导致充放电过程中，离子嵌入/脱出的动力学性能较差.  因此，电池电极材料的选择面临着新的挑战.  在对钾离子电池电极材料进行分类和总结的基础之上，重点介绍了石墨及各种形式的碳材料、过渡金属氧化物、合金类等负极材料以及普鲁士蓝、层状金属氧化物、聚阴离子型化合物等正极材料的研究进展，并对钾离子电池的发展进行了展望，以期对高性能钾离子电池的发展提供新思路."
    # query = "钠离子电池与锂离子电池的储能机理十分相似。由于钠离子电池具有成本低和钠资源丰富等优势，引起了人们的广泛关注，随着研究的进一步深入，有望在未来取代锂离子电池被广泛应用。为获得高性能钠离子电池，研究和开发比容量高、倍率性能好和循环性能优异的储钠电极材料势在必行。作为嵌入型负极材料的钛铌氧族化合物(TNO，包括 TiNb2O7和 Ti2Nb2O9等)具有良好的钠储存能力，近年来得到了研究人员的关注并取得了一定进展。综述了 TNO作为钠离子电池负极材料最新研究进展，简述了 TNO 材料的研究历史，分析了材料结构，介绍了 TNO 在钠离子电池方面取得的成果，探讨了研究过程中该材料存在的问题及改良方法，促进钠离子电池负极材料的开发。"
    
    query = """帮我把材料中影响阅读的文字删除，必须保留原文全部信息\n"{}\"， 
    """
    gen_model.gen_chat(query.format("中国人民大学学报1997年第6期’97保险与精算国际研讨会综述周伏平由中国人民大学统计学系主办的’97保险与精算国际研讨会于1997年6月下旬在中国人民大学举行。参加大会的有北美精算学会会长DavidHolland先生、前任会长HaroldIngarham先生、美国人寿保险管理学会副会长W．Rabel博士、美国天普大学荣誉教授段开龄先生、瑞士再保险公司总裁ReynaldBoutin先生、美国大都会人寿保险公司副总裁张源博士、国家教委高教司司长钟秉林、中国证监会监督管理委员会信息统计部主任徐雅萍、中国平安保险公司北京分公司总经理助理张国芳、中国人民大学副校长袁卫教授等10余位中外专家和领导。参加大会的还有中国人民大学统计学系、信息学院的广大师生。会议就风险的新思维、中美保险市场大扫描、保险与精算在中国的新发展等主题进行了广泛而深入的探讨。本文把主要内容综述如下：一、风险新思维保险和精算都是围绕风险这一核心而展开的，故而“何为风险”、“如何测定风险”是十分基础和重要的问题。大都会人寿保险公司远东地区副总裁张源博士对此提出了独到的见解。传统的风险定义为：风险就是未来事件的不确定性。在衡量风险大小时，总是事"))
    
    # query_model = Query_Model()
    # query_model.query_chat("写一篇新能源报告")
