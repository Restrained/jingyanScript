#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：import_mysql_chapter.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/5 上午10:28 
@explain : 文件说明
"""
import pandas as pd
from sqlalchemy import create_engine
import os


def read_csv_and_insert_to_mysql(csv_file, db_config, table_name, starting_chapter_id=847955):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file, encoding='gbk')

    # 添加额外的列
    df['chapter_id'] = range(starting_chapter_id, starting_chapter_id + len(df))
    df['chapter_vip'] = 1
    df['create_time'] = '2024-08-05'

    # 复制 matched_number 列为 chapter_num 和 chapter_order
    df['chapter_num'] = df['matched_number']
    df['chapter_order'] = df['matched_number']

    # 处理 new_file_path 列
    # df.drop(columns=['new_file_path'], inplace=True)
    df['content'] = df['new_file_path'].str.replace('F:\soundbook_files\\',
                                                    'https://listenmp3-1324534376.cos.ap-guangzhou.myqcloud.com/')

    # 重命名 file_path 列为 chapter_name 并提取文件名
    # df['chapter_name'] = df['file_path'].apply(lambda x: os.path.splitext(os.path.basename(x))[0])

    # 添加新的列并填充为 None
    df['last_update_time'] = None
    df['update_by'] = None
    df['update_time'] = None

    # 选择需要的列
    df = df[['chapter_id', 'book_id', 'chapter_vip', 'chapter_num', 'chapter_name', 'chapter_order', 'content',
             'last_update_time', 'update_by', 'create_time', 'update_time'

             ]]

    # 创建数据库连接字符串
    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

    # 创建数据库引擎
    engine = create_engine(connection_string)

    # 将数据写入 MySQL 表
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print(f"Data successfully inserted into {table_name}.")


# 示例调用
csv_file = 'update_book_info_v2.csv'  # 将 your_file.csv 替换为你的 CSV 文件路径
db_config = {
    'host': '193.112.190.33:3306',
    'user': 'bmsh',
    'password': 'htWetMfTh6Ehin4h',
    'database': 'bmsh'
}
table_name = 'u_book_read_chapter_info_listen'  # 替换为你的表名

read_csv_and_insert_to_mysql(csv_file, db_config, table_name)
