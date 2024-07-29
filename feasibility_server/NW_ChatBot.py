# coding: UTF-8
from write_query import *
from gen_query import *
import datetime

class NW_ChatBot:
    def __init__(self):
        self.write_model = Write_Model()
        self.gen_model = Gen_Model()
        self.query_model = Query_Model()

    def nw_chat(self, query="", mode = "all", section = ""):
        try:
            # 写作模块
            response_json = self.write_model.predict(query, mode, section, self.gen_model, self.query_model)
            return response_json
        except Exception as err:
            raise "Faild to pipeline inference error."
