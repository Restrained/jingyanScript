#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：data_migration.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/5 下午4:37 
@explain : 文件说明
"""
import pandas as pd
from sqlalchemy import create_engine


def transfer_data(source_db_config, target_db_config, query, table_name):
    # 连接到源数据库
    source_engine = create_engine(
        f"mysql+mysqlconnector://{source_db_config['user']}:{source_db_config['password']}@{source_db_config['host']}:{source_db_config['port']}/{source_db_config['database']}")

    # 连接到目标数据库
    target_engine = create_engine(
        f"mysql+mysqlconnector://{target_db_config['user']}:{target_db_config['password']}@{target_db_config['host']}:{target_db_config['port']}/{target_db_config['database']}")

    # 从源数据库读取数据
    df = pd.read_sql(query, con=source_engine)

    # 将数据插入到目标数据库
    df.to_sql(name=table_name, con=target_engine, if_exists='append', index=False)

    print(f"Data transferred to table {table_name} successfully.")


# 示例调用
source_db_config = {
    'user': 'source_db_user',
    'password': 'source_db_password',
    'host': 'source_db_host',
    'port': 3306,
    'database': 'source_db_name'
}

target_db_config = {
    'user': 'target_db_user',
    'password': 'target_db_password',
    'host': 'target_db_host',
    'port': 3306,
    'database': 'target_db_name'
}

query = """
    SELECT * 
    FROM u_book_read_chapter_info_listen 
    WHERE create_time = '2024-08-05 00:00:00'
"""

table_name = 'u_book_read_chapter_info_listen'

transfer_data(source_db_config, target_db_config, query, table_name)
