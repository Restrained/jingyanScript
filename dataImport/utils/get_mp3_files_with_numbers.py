#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：jingyanScript 
@File    ：get_mp3_files_with_numbers.py
@IDE     ：PyCharm 
@Author  ：Allen.Wan
@Date    ：2024/7/30 上午11:49 
@explain : 文件说明
"""
import os
import re
import pandas as pd


def get_mp3_files_with_numbers_in_subfolders(directory: str, output_csv_path: str, mismatch_excel_path: str):
    """
    针对指定目录下的下一级所有文件夹，读取其下的所有MP3文件名，提取其中的数字，找出目录下的最大数字，
    并将结果输出到一个CSV文件中。如果遇到文件匹配数字从小到大排列遇到缺失的情况
    或匹配到的数字文件总数不等于目录下最大数字的情况，则记录到Excel文件中。

    :param directory: 目标目录的路径
    :param output_csv_path: 输出CSV文件路径
    :param mismatch_excel_path: 记录不匹配情况的Excel文件路径
    """
    results = []
    mismatches = []

    # 获取指定目录下的下一级所有文件夹
    subfolders = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    # 正则表达式模式
    number_pattern1 = re.compile(r'第(\d+)集')
    number_pattern2 = re.compile(r'(\d+)集')
    number_pattern3 = re.compile(r'(\d+)')

    for subfolder in subfolders:
        mp3_files = []

        # 递归读取子文件夹中的所有MP3文件
        for root, _, files in os.walk(subfolder):
            for file in files:
                if file.endswith('.mp3'):
                    file_path = os.path.join(root, file)
                    filter_name = file.split('.')[0]
                    match = number_pattern1.search(filter_name)
                    if not match:
                        match = number_pattern2.search(filter_name)
                    if not match:
                        match = number_pattern3.search(filter_name)

                    if match:
                        number = int(match.group(1))
                        mp3_files.append((file_path, number))

        if not mp3_files:
            print(f"No MP3 files found with numbers in the directory: {subfolder}")
            continue

        mp3_files.sort(key=lambda x: x[1])
        numbers = [file[1] for file in mp3_files]
        max_number = max(numbers)

        # 检查文件匹配数字从小到大排列是否有缺失
        missing_numbers = set(range(1, max_number + 1)) - set(numbers)
        if missing_numbers:
            mismatches.append({
                'subfolder': subfolder,
                'matched_count': len(numbers),
                'max_number': max_number,
                'missing_numbers': ', '.join(map(str, sorted(missing_numbers)))
            })
            print(f"Missing numbers in the sequence in {subfolder}: {sorted(missing_numbers)}")

        # 检查匹配到的数字文件总数是否等于目录下最大数字
        if len(numbers) != max_number:
            print(f"Number of matched files ({len(numbers)}) does not equal the max number ({max_number}) in the directory: {subfolder}")
            mismatches.append({
                'subfolder': subfolder,
                'matched_count': len(numbers),
                'max_number': max_number,
                'missing_numbers': ', '.join(map(str, sorted(missing_numbers)))
            })

        # 收集结果
        for file_path, number in mp3_files:
            results.append((subfolder, file_path, number, max_number))

    # 输出结果到CSV文件
    df_results = pd.DataFrame(results, columns=['subfolder', 'file_path', 'matched_number', 'max_number'])
    df_results.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Results have been written to {output_csv_path}")

    # 输出不匹配情况到Excel文件
    if mismatches:
        df_mismatches = pd.DataFrame(mismatches)
        df_mismatches.to_excel(mismatch_excel_path, index=False)
        print(f"Mismatch information has been written to {mismatch_excel_path}")

# 示例用法
if __name__ == "__main__":
    target_directory = r"F:\BaiduNetdiskDownload\【惊雁交音】"  # 替换为你目标目录的路径
    output_csv = "mp3_files_with_numbers.csv"  # 输出CSV文件的路径
    mismatch_excel = "mismatch_info.xlsx"  # 不匹配情况记录的Excel文件路径
    get_mp3_files_with_numbers_in_subfolders(target_directory, output_csv, mismatch_excel)
