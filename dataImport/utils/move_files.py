#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：move_files.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/2 上午11:14 
@explain : 文件说明
"""
import pandas as pd
import shutil
import os


def copy_files_and_update_csv(csv_file, destination_dir, new_csv_file):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file)

    # 创建目标目录（如果不存在）
    os.makedirs(destination_dir, exist_ok=True)

    # 初始化一个新的列用于存储新的文件路径
    df['new_file_path'] = ''

    # 遍历每一行，复制文件并重命名
    for index, row in df.iterrows():
        # 获取原始文件路径和新的文件名
        original_file_path = row['file_path']
        new_file_name = f"{row['new_file_name']}.mp3"  # 确保添加 .mp3 后缀

        # 构建新的文件路径
        new_file_path = os.path.join(destination_dir, new_file_name)

        # 检查目标目录中是否已经存在相同的文件
        if os.path.exists(new_file_path):
            df.at[index, 'new_file_path'] = new_file_path  # 更新新的文件路径到 DataFrame
            print(f"File already exists: {new_file_path}")
            continue

        # 复制并重命名文件
        try:
            shutil.copy(original_file_path, new_file_path)
            df.at[index, 'new_file_path'] = new_file_path  # 更新新的文件路径到 DataFrame
        except FileNotFoundError:
            print(f"File not found: {original_file_path}")
        except Exception as e:
            print(f"Error copying file {original_file_path} to {new_file_path}: {e}")

    # 将更新后的 DataFrame 保存到新的 CSV 文件中
    df.to_csv(new_csv_file, index=False)

    print(f"Files copied and new CSV saved successfully to {new_csv_file}.")


# 示例调用
csv_file = 'book_info.csv'  # 将 your_file.csv 替换为你的 CSV 文件路径
destination_dir = r'F:\soundbook_files'  # 替换为你的目标目录
new_csv_file = 'update_book_info.csv'  # 将 new_file.csv 替换为你想要保存的新 CSV 文件路径

copy_files_and_update_csv(csv_file, destination_dir, new_csv_file)

# 示例调用


