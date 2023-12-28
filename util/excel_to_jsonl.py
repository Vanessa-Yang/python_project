# -*- coding: utf-8 -*-
import glob

import pandas as pd
import json


def write_jsonl():
    # 读取Excel文件
    excel_file_path = 'E:\\百度文心一言模型微调_训练数据集\\SFT一阶段Lora训练\\AI训练问答（专篇工程）1227.xlsx'
    df = pd.read_excel(excel_file_path)

    # 将DataFrame转换为JSON格式
    json_list = []
    for index, row in df.iterrows():
        # prompt = row['prompt'] + "是什么，请详细说明？"
        prompt = row['prompt']
        response = [[row['response']]]
        entry = {"prompt": prompt, "response": response}
        # entry = {"prompt": prompt}
        entry_list = [entry]
        json_list.append(entry_list)

    # 将JSON数据保存到文件
    json_file_path = 'E:\\百度文心一言模型微调_训练数据集\\SFT一阶段Lora训练\\AI训练问答（专篇工程）1227.jsonl'
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        for item in json_list:
            # 打印转换后的JSON格式数据
            print(item)
            json.dump(item, json_file, ensure_ascii=False)
            json_file.write('\n')


def read_jsonl():
    a = 0
    # with open('C:\\Users\\Administrator\\Downloads\\sample-text-dialog-unsort-annotated.jsonl', 'r', encoding="utf-8") as f:
    with open('E:\\百度文心一言模型微调_训练数据集\\SFT一阶段Lora训练\\AI训练问答（专篇工程）1227.jsonl', 'r', encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            a = a + 1
            print(a, data)

# def merge_jsonl():
#     with open("E:\\百度文心一言模型微调_训练数据集\\SFT一阶段Lora训练\\merge.jsonl", "w", encoding="utf-8") as outfile:
#         for filename in glob.glob("E:\\百度文心一言模型微调_训练数据集\\SFT一阶段Lora训练\\*.jsonl"):
#             with open(filename, encoding="utf-8") as infile:
#                 for line in infile:
#                     outfile.write(line)
#                 if not line.endswith('\n'):
#                     outfile.write('\n')
#         print("finish...")


if __name__ == '__main__':
    # write_jsonl()
    read_jsonl()
    # merge_jsonl()