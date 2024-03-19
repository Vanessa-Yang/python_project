import os

import pandas as pd
import json


def extract_excel_data():
    keywords = ["施工工序", "注意事项", "验收标准", "安装前提", "工艺流程", "控制要点", "施工前提", "位置"]
    all_sheet_data = {}

    # 读取Excel文件
    excel_folder = 'E:\\百度文心一言模型微调_训练数据集\\20240102 AI训练问答表（无序号）\\'
    for filename in os.listdir(excel_folder):
        if not filename.endswith('.xlsx') and not filename.endswith(
                '.xls') or filename == '20240102 AI训练问答（住宅室内装饰装修设计规范 JGJ 367-2015）无序号':
            continue
        df = pd.read_excel(excel_folder + filename)

        for index, row in df.iterrows():
            kw = "其他"
            for keyword in keywords:
                if keyword in row['prompt']:
                    kw = keyword
                    break
            if not all_sheet_data.get(kw):
                # all_sheet_data[kw] = [['prompt', 'response']]
                all_sheet_data[kw] = []
            # idx = len(all_sheet_data[kw])
            all_sheet_data[kw].append([row['prompt'], row['response']])

    # 分组写入excel不同表单
    print("test")
    out_excel_path = 'E:\\百度文心一言模型微调_训练数据集\\20240102 AI训练问答表（无序号） - 提问类型分组\\提问关键词分组.xlsx'
    writer = pd.ExcelWriter(out_excel_path)

    keywords.append("其他")
    for sheet_name in keywords:
        data = all_sheet_data.get(sheet_name)
        if data:
            sheet = pd.DataFrame(data, columns=['prompt', 'response'])
            sheet.to_excel(writer, sheet_name=sheet_name, index=False)
    # 刷入磁盘
    writer.close()
    print("finish")


if __name__ == '__main__':
    extract_excel_data()
