#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：detele_repeat.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/1 下午3:56 
@explain : 文件说明
"""
import os

def delete_files_with_pattern(directory: str, pattern: str = '(1)'):
    """
    遍历指定目录及其子目录，删除所有包含指定模式的文件。

    :param directory: 目标目录的路径
    :param pattern: 要匹配的模式字符串，默认值为 '(1)'
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if pattern in file:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# 示例用法
if __name__ == "__main__":
    target_directory = r"F:\BaiduNetdiskDownload\【惊雁交音】\1633=权妃之帝医风华（新版）"  # 将此路径替换为你目标目录的路径
    delete_files_with_pattern(target_directory)

