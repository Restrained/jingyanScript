#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：store_api_response_in_db.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/7/22 下午2:51 
@explain : 获取畅读接口返回内容，解析后存到指定数据库表
"""
import pandas as pd

from utils.common import Database


class BookInfo:
    @staticmethod
    def read_csv(file_path):
        df = pd.read_csv(file_path)
        return df

    @staticmethod
    def wash_book_name(raw_book_name):
        book_name = raw_book_name.replace('《', '').replace('》', '')
        book_name = book_name.strip()
        return book_name

    @staticmethod
    def wash_book_id(raw_book_id):
        book_id = '8000' + str(raw_book_id)
        return book_id

    @staticmethod
    def wash_file_path(raw_book_id):
        book_id = '8000' + str(raw_book_id)
        return book_id

    def set_data(self, df):
        # book_id, book_name, author_name, nclass, nclass_id, chapter_num, labels, cover_path
        grouped = df.groupby(['directory_id', 'new_name', 'intro']).size().reset_index(name='count')
        grouped.rename(columns={'directory_id': 'book_id', 'new_name': 'book_name', 'count': 'chapter_num'},
                       inplace=True)

        # 整理原book_id及book_name
        grouped['book_id'] = grouped['book_id'].apply(
            lambda x: self.wash_book_id(x)
        )
        grouped['book_name'] = grouped['book_name'].apply(
            lambda x: self.wash_book_name(x)
        )
        grouped['intro'] = grouped['intro'].apply(
            lambda x: x.strip()
        )

        grouped['channel_id'] = None
        grouped['type'] = 1
        # grouped['author_name'] = None
        grouped['genre'] = None
        grouped['genre_id'] = None
        # grouped['nclass'] = None
        # grouped['nclass_id'] = 204
        grouped['book_status'] = None
        grouped['last_update_time'] = None
        grouped['book_num'] = None
        grouped['is_vip'] = None
        # grouped['labels'] = None
        grouped['roles'] = None
        grouped['hits'] = 0
        grouped['is_daily_recommendation'] = 0
        grouped['is_recommended'] = 0
        grouped['is_highly_rated'] = 0
        grouped['is_reputation'] = 0
        grouped['is_popular'] = 0
        grouped['create_time'] = None
        grouped['status'] = 1
        grouped['update_time'] = None
        grouped['score'] = None
        grouped['is_featured'] = None

        # 动态生成 cover_path 的链接
        # grouped['cover_path'] = grouped['book_id'].apply(
        #     lambda x: f"https://duanju-1324534376.cos.ap-guangzhou.myqcloud.com/cover-{x}.jpg")

        # 将结果转换为包含字典的列表

        # db_connection = create_engine('mysql+pymysql://bmsh:htWetMfTh6Ehin4h@193.112.190.33:3306/bmsh')
        database = Database(username='bmsh', password='htWetMfTh6Ehin4h', host='193.112.190.33:3306', db='bmsh')

        # 将 DataFrame 插入到指定的表中
        grouped.to_sql('u_book_info', con=database.create_mysql_engine(), if_exists='append', index=False)
