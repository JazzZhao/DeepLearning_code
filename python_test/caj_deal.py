# -*- coding: utf-8 -*-
from gen_query import *
import fitz  # PyMuPDF

gen_model = Gen_Model()
folder_path = "E:\\1workSpace\\thinkit\\south network\\datasets"
result_path = "E:\\1workSpace\\thinkit\\south network\\caj_data_result"


file_path = folder_path+'\\AI绘画研究综述_张泽宇.caj'

doc = fitz.open(file_path)

text = ""
for page in doc:
    text += page.get_text()

print(text)


