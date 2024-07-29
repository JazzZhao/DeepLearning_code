# -*- coding: utf-8 -*-
import os
import re
import fitz
import pdfplumber
from gen_query import *

gen_model = Gen_Model()
folder_path = "E:\\1workSpace\\thinkit\\south_network\\caj_data_pdf_2\\LLM"
result_path = "E:\\1workSpace\\thinkit\\south_network\\caj_data_result_2\\LLM"
# 遍历文件夹并打印所有文件名
# for filename in os.listdir(folder_path):
#     filepath = os.path.join(folder_path, filename)
#     print("读取的文件地址：" + filepath)
#     # 打开文件，并将内容追加到文件末尾
#     result_file_name, f = os.path.splitext(filename)
#     result_file_name = result_file_name + ".txt"
#     if os.path.exists(os.path.join(result_path, result_file_name)):
#         os.remove(os.path.join(result_path, result_file_name))
#         print("文件存在")
#     with fitz.open(filepath) as pdf:
#         num_pages = pdf.page_count
#         # is_page_end = False
#         for page_num in range(num_pages):
#             text = ""
#             start_tag = False
#             end_tag = False
#             # 每一页的开头和结尾判断一行的字数，小于20个字的过滤掉
#             page = pdf.load_page(page_num)
#             #删除开头
#             # start_num = -1
#             for block in page.get_text("dict")['blocks']:
#                 # start_num += 1
#                 if 'lines' in block:
#                     line_num = 0
#                     line_text = ""
#                     for line in block['lines']:
#                         for span in line['spans']:
#                             line_text += span['text']
#                             line_num += len(span['text'])
#                     if "参考文献" in line_text.replace(" ", "") and line_num<8:
#                         end_tag = True
#                     if page_num==0 and "摘要" in line_text.replace(" ", ""):
#                         start_tag = True
#                     if end_tag:
#                         break
#                     if line_num >= 15 and (not page_num ==0 or start_tag):
#                         for line in block['lines']:
#                             for span in line['spans']:
#                                 text += span['text']
#             with open(os.path.join(result_path, result_file_name), "a", encoding='utf-8') as f:
#                 f.write(text)
#             print(text)
#             if end_tag:
#                 break

#改名
# for filename in os.listdir(folder_path):
#     filepath = os.path.join(folder_path, filename)
#     if ".pdf" not in filepath:
#         filepath = filepath + ".pdf"
#         os.rename(os.path.join(folder_path, filename), filepath)

#读取单个文件
# filepath = os.path.join(folder_path, "BIM技术在装配式建筑中的应用研究综述.pdf")
# doc = fitz.open(filepath)
# # 获取 PDF 文件中的页面数量
# num_pages = doc.page_count
# for page_num in range(num_pages):
#     page = doc.load_page(page_num)
#     text = page.get_text("text")
#     print(f"Page {page_num+1}:")
#     print(text)
# # 关闭 PDF 文件
# doc.close()

# 获取摘要
# for filename in os.listdir(folder_path):
#     filepath = os.path.join(folder_path, filename)
#     print("读取的文件地址：" + filepath)
#     # 打开文件，并将内容追加到文件末尾
#     result_file_name, f = os.path.splitext(filename)
#     result_file_name = result_file_name + ".txt"
#     if os.path.exists(os.path.join(result_path, result_file_name)):
#         os.remove(os.path.join(result_path, result_file_name))
#         print("文件存在")
#     with fitz.open(filepath) as pdf:
#         num_pages = pdf.page_count
#         # is_page_end = False
#         for page_num in range(num_pages):
#             start_tag = False
#             end_tag = False
#             result = ""
#             # 每一页的开头和结尾判断一行的字数，小于20个字的过滤掉
#             page = pdf.load_page(page_num)
#             text = page.get_text("text").replace(" ", "").replace("\n", "")
#             pattern = r"摘要(.*?)关键词"
#             # 使用正则表达式匹配
#             match = re.search(pattern, text, re.DOTALL)
#             if match:
#                 end_tag = True
#                 result = match.group(1).strip()
#                 print("摘要和关键词之间的内容：", result)
#             else:
#                 print("未找到匹配的内容")
#             #删除开头
#             # start_num = -1
#             # for block in page.get_text("dict")['blocks']:
#             #     # start_num += 1
#             #     if 'lines' in block:
#             #         line_num = 0
#             #         line_text = ""
#             #         for line in block['lines']:
#             #             for span in line['spans']:
#             #                 line_text += span['text']
#             #         if "关键词" in line_text.replace(" ", ""):
#             #             end_tag = True
#             #         if "摘要" in line_text.replace(" ", ""):
#             #             start_tag = True
#             #         if start_tag:
#             #             text += line_text    
#             #         if end_tag:
#             #             break
#             with open(os.path.join(result_path, result_file_name), "a", encoding='utf-8') as f:
#                 f.write(result)
#             if end_tag:
#                 break

def count_chinese(text):
    chinese_chars = 0
    total_chars = 0
    
    for char in text:
        # 判断字符是否为英文字母或者标点符号
        if '\u4e00' <= char <= '\u9fff':
            chinese_chars += 1
        # 忽略空格等非文本字符
        if char.strip():
            total_chars += 1
    
    # 计算英文比例
    chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0
    
    return chinese_chars, total_chars, chinese_ratio

def split_text(
    text: str, max_tokens: int, overlap: int = 0
):
    """
    Splits the input text into smaller chunks based on the tokenizer and maximum allowed tokens.
    
    Args:
        text (str): The text to be split.
        max_tokens (int): The maximum allowed tokens.
        overlap (int, optional): The number of overlapping tokens between chunks. Defaults to 0.
    
    Returns:
        List[str]: A list of text chunks.
    """
    # Split the text into sentences using multiple delimiters
    delimiters = ["。", "！", "？",".","!","?", "\n"]
    regex_pattern = "|".join(map(re.escape, delimiters))
    sentences = re.split(regex_pattern, text)
    
    # Calculate the number of tokens for each sentence
    n_tokens = [len(sentence) for sentence in sentences]
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence, token_count in zip(sentences, n_tokens):
        # If the sentence is empty or consists only of whitespace, skip it
        if not sentence.strip():
            continue
        
        # If the sentence is too long, split it into smaller parts
        if token_count > max_tokens:
            sub_sentences = re.split(r"[,;:，：；]", sentence)
            sub_token_counts = [len(sub_sentence) for sub_sentence in sub_sentences]
            
            sub_chunk = []
            sub_length = 0
            
            for sub_sentence, sub_token_count in zip(sub_sentences, sub_token_counts):
                if sub_length + sub_token_count > max_tokens:
                    chunks.append(" ".join(sub_chunk))
                    sub_chunk = sub_chunk[-overlap:] if overlap > 0 else []
                    sub_length = sum(sub_token_counts[max(0, len(sub_chunk) - overlap):len(sub_chunk)])
                sub_chunk.append(sub_sentence)
                sub_length += sub_token_count
            
            if sub_chunk:
                chunks.append(" ".join(sub_chunk))
        
        # If adding the sentence to the current chunk exceeds the max tokens, start a new chunk
        elif current_length + token_count > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
            current_length = sum(n_tokens[max(0, len(current_chunk) - overlap):len(current_chunk)])
            current_chunk.append(sentence)
            current_length += token_count
        
        # Otherwise, add the sentence to the current chunk
        else:
            current_chunk.append(sentence)
            current_length += token_count
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

# 通过大模型过滤掉一些乱码
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    print("读取的文件地址：" + filepath)
    # 打开文件，并将内容追加到文件末尾
    result_file_name, f = os.path.splitext(filename)
    result_file_name = result_file_name + ".txt"
    if os.path.exists(os.path.join(result_path, result_file_name)):
        # os.remove(os.path.join(result_path, result_file_name))
        print("文件存在")
        continue
    with fitz.open(filepath) as pdf:
        num_pages = pdf.page_count
        # is_page_end = False
        for page_num in range(num_pages):
            start_tag = False
            end_tag = False
            result = ""
            # 每一页的开头和结尾判断一行的字数，小于20个字的过滤掉
            page = pdf.load_page(page_num)
            text = page.get_text("text").replace(" ", "").replace("\n", "")
            text_list = split_text(text=text, max_tokens=500)
            for pre_deal_text in text_list:
                # 使用正则表达式匹配
                query = """帮我用中文重写下面这段话：\n\"{}\"\n注： 越详细越好，要完整体现文章全部要点
                        """
                chinese_chars, total_chars, chinese_ratio = count_chinese(pre_deal_text)
                print("处理前文字："+query.format(pre_deal_text))
                if len(pre_deal_text) < 100 or chinese_ratio < 0.6:
                    continue
                model_result = gen_model.gen_chat(query.format(pre_deal_text),gen_hist=[])
                while "帮我用中文重写下面这段话" in model_result["answer"].text:
                    model_result = gen_model.gen_chat(query.format(pre_deal_text), gen_hist=[])
                result += model_result["answer"].text
            with open(os.path.join(result_path, result_file_name), "a", encoding='utf-8') as f:
                f.write(result)

# if __name__ == "__main__":
#     text = "[1]普通高中地理课程标准(2017年版2020年修订)『M]．北京：人民教育出版社，2021．[2]谢欢芳．地理实践力视域下的校内地理课程资源开发——以“形色”App运用于校园植物调查为例Ⅱ]．地理教育，2020(2)：51-52．[3]丁洁．辽宁省中小学综合实践基地(学校)效能研究『D]．沈阳：沈阳师范大学，2017．[4]张琳娴．基于地理实践力的乡土研学方案设计与实践——以四明山研学旅行为例卟地理教学，2021(18)：46—49．[14】邱悦，朱世琴，范丹丹．基于多维指标融合的中文图书质量评价体系构建研究Ⅱ】．图书馆杂志，2021，40(03)：109—115．[10]刘运梅，李长玲，杜德慧．网络环境下论文影响力综合评价体系构建——基于时间因素视角Ⅱ1．情报资料工作，2019，40(06)：16—22．[15】朱世琴，邱悦，陈红英．融入评论指标的中文图书综合评价体系适应性研究Ⅱ】．图书情报工作，2021，65(09)：23—31．"
#     chinese_chars, total_chars, chinese_ratio = count_chinese(text=text)
#     print(chinese_ratio)
#     print(chinese_chars)
#     print(total_chars)
