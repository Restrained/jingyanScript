#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：second_check.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/8/2 上午10:13 
@explain : 文件说明
"""
import pandas as pd


def check_matched_numbers(csv_file):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file, encoding='utf-8')

    # 以 subfolder 列进行分组
    grouped = df.groupby('subfolder')

    # 初始化一个空列表用于存储结果
    results = []

    # 遍历每个组
    for name, group in grouped:
        # 统计 matched_number 的值出现的次数
        count = group['matched_number'].value_counts()

        # 检查是否存在出现次数大于 2 的情况
        over_2_count = count[count > 1]

        # 检查 matched_number 是否从小到大存在中间缺失的情况
        sorted_numbers = sorted(group['matched_number'].unique())
        missing_numbers = set(range(sorted_numbers[0], sorted_numbers[-1] + 1)) - set(sorted_numbers)

        if not over_2_count.empty or missing_numbers:
            results.append((name, over_2_count, sorted_numbers, missing_numbers))

    return results


# 示例调用
csv_file = 'mp3_files_with_numbers.csv'  # 将 your_file.csv 替换为你的 CSV 文件路径
results = check_matched_numbers(csv_file)

# 打印结果
print(results)