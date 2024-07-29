# -*- coding: utf-8 -*-
from NW_ChatBot import NW_ChatBot
from gen_write_template import WriteDocxInference
from flask import Flask, request, Response, stream_with_context
import logging
import traceback
import json
import datetime
import numpy as np
import decimal
import uuid

import get_logger

# 示例化flask对象和初始化日志对象
app = Flask(__name__)
get_logger.log_file(logging.INFO)

chatbot = NW_ChatBot()
# write_docx_infer = WriteDocxInference()

class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        如有其他的需求可直接在下面添加
        :param obj:
        :return:
        """
        if isinstance(obj, datetime.datetime):
            # 格式化时间
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.date):
            # 格式化日期
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, decimal.Decimal):
            # 格式化高精度数字
            return float(obj)
        if isinstance(obj, uuid.UUID):
            # 格式化uuid
            return str(obj)
        if isinstance(obj, bytes):
            # 格式化字节数据
            return obj.decode("utf-8")
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return json.JSONEncoder.default(self, obj)

@app.route('/feasibility_report', methods=['POST'])
def predict():
    try:
        params = request if isinstance(request, dict) else request.json
        query = params['query']
        mode = params['mode']
        section = params['section']
        response_json = chatbot.nw_chat(query=query, mode= mode, section=section)
        logging.info("Model prediction completed.")
        def generate(response_json, query):
            try:
                logging.info("response type: {}".format(type(response_json)))
                text = ""
                for response in response_json:
                    if not response["answer"]:
                        return Response(json.dumps({"code": -1, "error_msg": "Faild to predict."}))
                    iterator = response.pop("answer")  # 迭代器对象
                    for chunk in iterator.iter_content(1024):
                        words = chunk.decode("utf-8", "ignore")
                        # print('------------words-----------', words)
                        text += words
                        response["answer"] = words
                        # yield json.dumps(words, cls=JSONEncoder, ensure_ascii=False)
                text = text.replace('\n\n', '\n')
                print(text)
                return json.dumps(text, cls=JSONEncoder, ensure_ascii=False)
            except Exception as err:
                logging.error("Handle iteration process failure")
                logging.error(traceback.format_exc())
                return json.dumps({"code": "-1", "error_msg": "Faild to predict."})
        return Response(generate(response_json, query))
    except Exception as err:
        logging.error(traceback.format_exc())
        return Response(json.dumps({"code": "-1", "error_msg": "Faild to predict."}))


@app.after_request
def after_request(response):
    # response.headers['Content-Type'] = 'text/event-stream' 
    # response.headers['Transfer-Encoding'] = 'chunked' 
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=63000, debug=True)
    # response_json = chatbot.nw_chat("我想写一篇关于电池的研究报告")
    # response_json = chatbot.nw_chat("我想写一篇关于电池的研究报告，锂离子电池（LIBS）已经广泛应用到便携式电子产品和电动汽车上.  \
    #                                 然而，随着锂资源的开采使用，锂离子电池的成本也在逐渐增加.  相比之下，地壳中较高的钾含量使\
    #                                 得钾离子电池（KIB）成本相对较低.  进而，钾离子电池作为一种新型低成本储能器件受到了广泛关注. \
    #                                  但钾离子的半径较大，导致充放电过程中，离子嵌入/脱出的动力学性能较差.  因此，电池电极材料的\
    #                                 选择面临着新的挑战.  在对钾离子电池电极材料进行分类和总结的基础之上，重点介绍了石墨及各种形\
    #                                 式的碳材料、过渡金属氧化物、合金类等负极材料以及普鲁士蓝、层状金属氧化物、聚阴离子型化合物等\
    #                                 正极材料的研究进展，并对钾离子电池的发展进行了展望，以期对高性能钾离子电池的发展提供新思路.")
    # response_json = chatbot.nw_chat("我想写一篇关于电池的研究报告，锂离子电池#电池管理系统（BMS）#荷电状态（SOC）#综述\
    #                                 #基于模型的估计#基于数据的估计#锂离子电池#爆炸机理#致爆时间#加热#过充#短路\
    #                                 #充放电#产热#硫正极#锂硫电池#综述#金属硫化物#有机硫化物#研究进展\
    #                                 #钾离子电池#负极材料#正极材料#高性能#钠离子电池#钛铌氧族化合物#质子交换膜燃料电池( PEMFC)#控制\
    #                                 #控制策略#水系锌离子电池#锌负极#碳材料#电动汽车#动力电池#振动与冲击#液态金属电极#储能电池#电解质材料\
    #                                 #水系镁离子电池#水系电解液#电极材料#储能#工业化#高效#太阳能电池#PN 型#文献计量分析#有机废水#能量回收#微生物燃料电池（MFC）\
    #                                 #固体氧化物燃料电池;阴极材料;钙钛矿氧化物#钙钛矿太阳能电池#空穴传输材料#光电转换效率#填充因子#CIGS#薄膜")
    # response_json = chatbot.nw_chat("我想写一篇关于电池的研究报告,本文总结了锂离子电池SOC估计方法的最新研究和硫正极材料等关键领域的进展，以及钾离子电池和钠离子电池的挑战和研究方向。")
    # response_json = chatbot.nw_chat("我想写一篇关于电池的研究报告，#锂离子电池热失效机理和致爆时间研究综述##综述##锂离子电池##爆炸机理##致爆时间##加热##过充##短路\
                                    # ")
    # fill_template_dict = {}  # 构造写入模板的字典数据
    # for response in response_json:
    #     placeholder_name = response.pop("placeholder_name")   # 占位符
    #     fill_template_dict[placeholder_name] = response.pop("answer").text
    # write_docx_infer.write_to_template(fill_template_dict)
    # result = gen_chat(query=first_feasibility_report_prompt)
    # print(result.text)

