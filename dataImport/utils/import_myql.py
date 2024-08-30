#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：import_myql.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/2 上午10:26 
@explain : 文件说明
"""
import os

import pandas as pd
from sqlalchemy import create_engine

import requests
import hashlib


def download_image(cover_path, save_dir, file_name):
    # 生成保存路径
    save_path = os.path.join(save_dir, file_name)

    # 下载图片
    response = requests.get(cover_path, stream=True)

    if response.status_code == 200:
        # 保存图片到本地路径
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image saved to {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def get_book_info(book_id):
    spid = "1022"
    client_id = "bimoshenghua1022"
    client_secret = "cff3e65d1ecc9b9433fe9ccbdea6a46a5864ac5a"

    # 生成sign
    sign_str = client_id + client_secret + book_id
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    # 构建请求的URL
    url = "http://api2.yuedunovel.com/listen/book/info"
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


def format_cover_url(original_url):
    # 提取路径部分（忽略协议和域名）
    path = original_url.replace('http://test.yuedunovel.com/', '')

    # 分割路径，提取目录和文件名
    parts = path.split('/')
    directory = parts[-2]  # 目录部分
    file_name = os.path.basename(parts[-1])  # 文件名部分

    # 格式化新的文件名
    new_file_name = f"listen-0-images-{directory}-{file_name}"

    # 拼接新的 URL
    new_url = f"https://pic20240312-1324534376.cos.ap-guangzhou.myqcloud.com/{new_file_name}"
    return new_url, new_file_name

def process_csv_and_import_to_mysql(csv_file, mysql_url, table_name):
    save_dir = r'C:\Users\1\Pictures\novel_cover'
    base_url = "https://pic20240312-1324534376.cos.ap-guangzhou.myqcloud.com/"
    # 读取 CSV 文件
    df = pd.read_csv(csv_file, encoding='utf-8')

    # 去除 subfolder 列中的特定字符
    df['subfolder'] = df['subfolder'].str.replace(r'^F:\\BaiduNetdiskDownload\\【惊雁交音】\\', '', regex=True)

    # 通过 = 字符分隔 subfolder 列
    df[['book_id', 'book_name']] = df['subfolder'].str.split('=', expand=True)

    # 重命名 max_number 列为 chapter_num
    df.rename(columns={'max_number': 'chapter_num'}, inplace=True)

    # 按照 subfolder 列进行分组，并保留 chapter_num 最大的那一行
    df = df.loc[df.groupby('subfolder')['chapter_num'].idxmax()]

    # 删除 subfolder 列
    df.drop(columns=['subfolder'], inplace=True)
    df.drop(columns=['file_path'], inplace=True)
    df.drop(columns=['matched_number'], inplace=True)

    df['channel_id'] = None
    df['type'] = 1
    # df['book_name'] = book_info.get('book_name')
    df['author_name'] = None
    df['intro'] = None
    df['genre'] = None
    df['genre_id'] = None
    df['nclass'] = None
    df['nclass_id'] = None
    df['book_status'] = None
    df['cover_path'] = None
    df['last_update_time'] = None
    df['book_num'] = None
    df['is_vip'] = None
    df['labels'] = None
    df['roles'] = None
    df['hits'] = None
    df['is_daily_recommendation'] = 0
    df['is_recommended'] = 0
    df['is_highly_rated'] = 0
    df['is_reputation'] = 0
    df['is_popular'] = 0
    df['create_time'] = '2024-08-05 00:00:00'
    df['status'] = 1
    df['update_time'] = None
    df['score'] = None
    df['is_featured'] = None
    df['sort'] = None
    df['is_pay'] = None
    df['is_vod'] = 0

    for index, row in df.iterrows():
        book_id = row['book_id']
        try:
            book_info = get_book_info(book_id)
            df.at[index, 'book_name'] = book_info.get('name')
            df.at[index, 'author_name'] = book_info.get('author')
            df.at[index, 'intro'] = book_info.get('brief')
            df.at[index, 'nclass'] = book_info.get('category')
            df.at[index, 'nclass_id'] = book_info.get('category_id')
            df.at[index, 'labels'] = book_info.get('keywords')

            # 处理 cover_path
            cover_path_url = book_info.get('cover')
            if cover_path_url:
                # 格式化 URL 和文件名
                new_cover_path, new_file_name = format_cover_url(cover_path_url)
                df.at[index, 'cover_path'] = new_cover_path

                # 下载图片
                download_image(cover_path_url, save_dir, new_file_name)

        except Exception as e:
            print(f"Error fetching book info for book_id {book_id}: {e}")

    # 创建 MySQL 引擎
    engine = create_engine(mysql_url)

    # 将数据导入到指定的 MySQL 表中
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    print(f"Data imported successfully into {table_name} table.")


# 示例调用
csv_file = 'mp3_files_with_numbers.csv'  # 将 your_file.csv 替换为你的 CSV 文件路径
mysql_url = 'mysql+mysqlconnector://bmsh:htWetMfTh6Ehin4h@193.112.190.33:3306/bmsh'  # 替换为你的 MySQL 连接字符串
table_name = 'u_book_info'  # 替换为你的 MySQL 表名

process_csv_and_import_to_mysql(csv_file, mysql_url, table_name)
