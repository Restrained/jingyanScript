import os
import re
from typing import Callable

import pandas as pd


class Utils:
    @staticmethod
    def remove_chinese_from_mp4(directory):
        """传入指定目录，将其中的mp4格式的文件名删除除数字以外的字符"""
        files = os.listdir(directory)
        for file_name in files:
            if file_name.endswith('.mp4'):
                mp4_file_path = os.path.join(directory, file_name)

                # Extract digits from the file name
                digits_only_name = ''.join(re.findall(r'\d+', os.path.splitext(file_name)[0])) + '.mp4'

                # Generate new file path with digits-only name
                new_mp4_file_path = os.path.join(directory, digits_only_name)

                os.rename(mp4_file_path, new_mp4_file_path)
                print(f"Renamed {mp4_file_path} to {new_mp4_file_path}")

    @staticmethod
    def rename_mov_to_mp4(directory):
        """传入指定目录, 将其中mov文件强制修改为mp4格式"""
        for file_name in os.listdir(directory):
            if file_name.endswith('.mov'):
                mov_file_path = os.path.join(directory, file_name)
                mp4_file_path = os.path.join(directory, os.path.splitext(file_name)[0] + '.mp4')

                os.rename(mov_file_path, mp4_file_path)
                print(f"Renamed {mov_file_path} to {mp4_file_path}")

    @staticmethod
    def update_file_paths(csv_path: str, column_name: str, process_function: Callable[[str], str],
                          output_csv_path: str) -> None:
        """
        此方法用于修改指定csv文件的每列内容，通过传入的处理函数进行替换，并输出一个新的csv

        :param csv_path: 原始CSV文件路径
        :param column_name: 需要处理的列名
        :param process_function: 用于处理每个列值的函数
        :param output_csv_path: 输出CSV文件路径
        :return: 修改后的DataFrame
        """
        # 读取CSV文件
        df = pd.read_csv(csv_path, encoding='gbk')

        # 使用传入的函数处理指定列
        df[column_name] = df[column_name].apply(process_function)

        # 保存修改后的CSV文件
        df.to_csv(output_csv_path, index=False, encoding='gbk')



