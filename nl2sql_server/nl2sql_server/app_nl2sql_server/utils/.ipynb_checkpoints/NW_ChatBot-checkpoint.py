# coding: UTF-8
from utils.write_query import *
from utils.gen_query import *

class NW_ChatBot:
    def __init__(self):
        self.write_model = Write_Model()
        self.gen_model = Gen_Model()
    def nw_chat(self, query="", mode = "all", section = ""):
        try:
            response_json = self.write_model.predict(query, mode, section, self.gen_model)
            return response_json
        except Exception as err:
            raise "Faild to pipeline inference error."