# -*- coding: utf-8 -*-
from flask import Flask, request, Response, stream_with_context
from utils import NW_ChatBot
import json
import logging
import traceback
from flask import Blueprint, Response
from utils import log_file
import datetime
import numpy as np
import decimal
import uuid
import re

log_file(logging.INFO)
nl2sql_blue = Blueprint('nl2sql', __name__)
chatbot = NW_ChatBot()
@nl2sql_blue.route('/nl2sql', methods=['POST'])
def predict():
    try:
        params = request if isinstance(request, dict) else request.json
        query = params['query']
        if "<nw_query>" in query and "<nw_source>" in query:
            query = re.findall(r"(?<=<nw_query>).*(?=<nw_source>)", query, re.DOTALL)[0]  # 用户问题
        response_json = chatbot.nw_chat(query=query)
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
                        yield json.dumps(response, cls=JSONEncoder, ensure_ascii=False)+"<nw_dict>"
                text = text.replace('\n\n', '\n')
                # logging.info(text)
                # return json.dumps(text, cls=JSONEncoder, ensure_ascii=False)
            except Exception as err:
                logging.error("Handle iteration process failure")
                logging.error(traceback.format_exc())
                yield json.dumps({"code": "-1", "error_msg": "Faild to predict."})
        return Response(generate(response_json, query))
    except Exception as err:
        logging.error(traceback.format_exc())
        return Response(json.dumps({"code": "-1", "error_msg": "Faild to predict."}))

@nl2sql_blue.after_request
def after_request(response):
    response.headers['Content-Type'] = 'text/event-stream' 
    response.headers['Transfer-Encoding'] = 'chunked' 
    return response


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        如有其他的需求可直接在下面添加
        :param obj:
        :return:
        """
        print(type(obj))
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