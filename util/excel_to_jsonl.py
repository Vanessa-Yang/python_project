# -*- coding: utf-8 -*-

import json
import os

import pandas as pd


def write_jsonl():
    # 读取Excel文件
    excel_file_path = 'E:\\百度文心一言模型微调_训练数据集\\20240102 AI训练问答表（无序号） - 提问类型分组\\提问关键词分组.xlsx'

    df = pd.read_excel(excel_file_path, sheet_name=None)

    # 将DataFrame转换为JSON格式
    sheet_idx = 0
    for sheet_name, data in df.items():
        json_list = []
        sheet_idx += 1
        for index, row in data.iterrows():
            # prompt = row['prompt'] + "是什么，请详细说明？"
            prompt = row['prompt']
            response = [[row['response']]]
            entry = {"prompt": prompt, "response": response}
            # entry = {"prompt": prompt}
            entry_list = [entry]
            json_list.append(entry_list)

        # 将JSON数据保存到文件
        json_file_path = f'E:\\百度文心一言模型微调_训练数据集\\20240102 AI训练问答表（无序号） - 提问类型分组\\提问关键词分组_{sheet_idx}{sheet_name}.jsonl'
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            for item in json_list:
                json.dump(item, json_file, ensure_ascii=False)
                json_file.write('\n')


def read_jsonl():
    idx = 0
    folder = 'E:\\百度文心一言模型微调_训练数据集\\20240102 AI训练问答表（无序号） - 提问类型分组\\'
    for filename in os.listdir(folder):
        if filename.startswith("提问关键词分组") and filename.endswith(".jsonl"):
            with open(folder + filename, 'r', encoding="utf-8") as f:
                for line in f:
                    idx += 1
                    data = json.loads(line)
                    print(idx, data)


if __name__ == '__main__':
    write_jsonl()
    read_jsonl()