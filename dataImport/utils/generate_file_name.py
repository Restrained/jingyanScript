#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：generate_file_name.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/2 上午11:05 
@explain : 文件说明
"""
import pandas as pd


def process_csv_and_save_new_file(csv_file, new_csv_file):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file, encoding='utf-8')

    # 去除 subfolder 列中的特定字符
    df['subfolder'] = df['subfolder'].str.replace(r'^F:\\BaiduNetdiskDownload\\【惊雁交音】\\', '', regex=True)

    # 通过 = 字符分隔 subfolder 列
    df[['book_id', 'book_name']] = df['subfolder'].str.split('=', expand=True)

    # 处理 matched_number 列，使其至少为4位，不足4位的前面补0
    df['matched_number'] = df['matched_number'].apply(lambda x: str(x).zfill(4))

    # 创建 new_file_name 列，将 book_id 和处理后的 matched_number 通过 - 连接
    df['new_file_name'] = df['book_id'] + '-' + df['matched_number']

    # 删除不需要的列
    # df.drop(columns=['subfolder', 'book_id', 'book_name'], inplace=True)

    # 保存处理后的数据到新的 CSV 文件中
    df.to_csv(new_csv_file, index=False)

    print(f"Data saved successfully to {new_csv_file}.")


# 示例调用
csv_file = 'mp3_files_with_numbers.csv'  # 将 your_file.csv 替换为你的 CSV 文件路径
new_csv_file = 'book_info.csv'  # 将 new_file.csv 替换为你想要保存的新 CSV 文件路径

process_csv_and_save_new_file(csv_file, new_csv_file)
