#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：get_chapter_name.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/5 下午5:03 
@explain : 文件说明
"""
import pandas as pd
import requests
import hashlib
import re


def get_book_info(book_id):
    spid = "1022"
    client_id = "bimoshenghua1022"
    client_secret = "cff3e65d1ecc9b9433fe9ccbdea6a46a5864ac5a"

    # 生成sign
    sign_str = client_id + client_secret + str(book_id)
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    # 构建请求的URL
    url = "http://api2.yuedunovel.com/listen/book/chapters"
    params = {
        "client_id": client_id,
        "spid": spid,
        "sign": sign,
        "book_id": book_id
    }

    # 发送请求
    response = requests.get(url, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def process_csv_and_match_chapters(csv_file, output_file):
    # 读取CSV文件
    df = pd.read_csv(csv_file, encoding='utf-8')

    # 创建一个字典以存储章节信息
    chapter_info_dict = {}

    # 遍历CSV文件中的每个book_id
    for book_id in df['book_id'].drop_duplicates():
        book_info = get_book_info(book_id)
        if isinstance(book_info, list):
            for chapter in book_info:
                name = chapter.get('name', '')
                number_pattern1 = re.compile(r'第(\d+)集')
                number_pattern2 = re.compile(r'(\d+)集')
                number_pattern3 = re.compile(r'(\d+)')

                match = number_pattern1.search(name)
                if not match:
                    match = number_pattern2.search(name)
                if not match:
                    match = number_pattern3.search(name)

                if match:
                    number = int(match.group(1))
                    chapter_info_dict[(book_id, number)] = name

    # 初始化新的章节名称列
    df['chapter_name'] = ''

    # 遍历CSV文件，匹配并更新章节名称
    for (book_id, number), chapter_name in chapter_info_dict.items():
        matched_rows = df[(df['book_id'] == book_id) & (df['matched_number'] == number)]
        for index in matched_rows.index:
            df.at[index, 'chapter_name'] = chapter_name

    # 保存结果到新的CSV文件
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Results saved to {output_file}.")


# 示例调用
csv_file = 'update_book_info.csv'
output_file = 'update_book_info_v2.csv'

process_csv_and_match_chapters(csv_file, output_file)

