#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：common.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/7/22 下午2:56 
@explain : 文件说明
"""
from dataclasses import dataclass

import pandas as pd
from sqlalchemy import create_engine


@dataclass
class Database:
    username: str
    password: str
    host: str
    db: str

    def create_mysql_engine(self):
        """
        取消注册该事件

        :return:
        """
        db_connection = create_engine(f'mysql+pymysql://{self.username}:{self.password}@{self.host}/{self.db}')
        return db_connection


class Toolkit:
    @staticmethod
    def df_to_db(db: Database, df: pd.DataFrame):
        df.to_sql(name=df.name, con=db.create_mysql_engine(), if_exists='append', index=False)
