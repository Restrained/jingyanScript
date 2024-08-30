import os
import re
import subprocess
import zipfile
from typing import List, Tuple, Dict

import pandas as pd





class BookInfo():

    def extract_zip_files_based_on_csv(self, directory: str, filtered_csv_path: str):
        """
        遍历指定目录下的文件夹，根据filtered_output.csv中的book_name进行ZIP文件解压。

        :param directory: 目标目录的路径
        :param filtered_csv_path: 过滤后的CSV文件路径
        """
        try:
            # 读取过滤后的CSV文件，获取所有book_name
            df = pd.read_csv(filtered_csv_path)
            target_books = df['book_name'].tolist()

            # 遍历指定目录下的文件夹
            for root, dirs, files in os.walk(directory):
                for folder in dirs:
                    folder_path = os.path.join(root, folder)
                    _, book_name = self.parse_folder_name(folder)

                    if book_name in target_books:
                        self.recursive_extract(folder_path)
        except Exception as e:
            print(f"An error occurred: {e}")

    def recursive_extract(self, folder_path: str):
        """
        递归解压目录中的所有ZIP文件。

        :param folder_path: 要解压的文件夹路径
        """
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_file:
                            for zip_info in zip_file.infolist():
                                try:
                                    # 如果是文件夹就直接创建目录
                                    if zip_info.filename.encode('cp437').decode('gbk')[-1] == '/':
                                        zip_file.extract(zip_info, root)
                                    else:
                                        try:
                                            # 如果是文件，先将文件名从gbk编码转换为utf-8编码
                                            zip_info.filename = zip_info.filename.encode('cp437').decode('gbk')
                                        except UnicodeDecodeError:
                                            # 如果gbk解码失败，尝试使用latin-1解码
                                            zip_info.filename = zip_info.filename.encode('cp437').decode('latin-1')
                                        zip_file.extract(zip_info, root)
                                except UnicodeDecodeError:
                                    print(f"Error: Cannot decode filename {zip_info.filename} in ZIP file {file_path}")
                                    continue  # 跳过无法解码的文件
                            print(f"Extracted {file} in {root}")
                    except zipfile.BadZipFile:
                        print(f"Error: Bad ZIP file {file_path}")
                    except zipfile.LargeZipFile:
                        print(f"Error: ZIP file {file_path} is too large")
                    except Exception as e:
                        print(f"An error occurred while extracting {file_path}: {e}")



    @staticmethod
    def parse_folder_name(folder_name: str) -> Tuple[str, str]:
        """
        解析文件夹名称，提取book_id和book_name。

        :param folder_name: 文件夹名称
        :return: (book_id, book_name)元组
        """
        parts = folder_name.split("=")
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return folder_name, ""  # 如果没有分隔符，则返回原始名称作为book_id

    @staticmethod
    def parse_folder_name(folder_name: str) -> Tuple[str, str]:
        """
        解析文件夹名称，提取book_id和book_name。

        :param folder_name: 文件夹名称
        :return: (book_id, book_name)元组
        """
        parts = folder_name.split("=")
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return folder_name, ""  # 如果没有分隔符，则返回原始名称作为book_id

    @staticmethod
    def get_mp3_count_and_max_chapter(directory: str) -> Tuple[int, int]:
        """
        获取指定目录及其子目录中的所有MP3文件数量，并减去文件名包含"(1)"的部分，
        同时查找文件名中的数字，取出最大的数字作为max_chapter_num。

        :param directory: 目标目录的路径
        :return: (MP3文件数量, 最大章节数字)
        """


        # 正则表达式模式
        number_pattern1 = re.compile(r'第(\d+)集')
        number_pattern2 = re.compile(r'(\d+)集')
        number_pattern3 = re.compile(r'(\d+)')


        mp3_files = []

        # 递归读取子文件夹中的所有MP3文件
        for root, _, files in os.walk(directory):
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

        count_numbers = [file[1] for file in mp3_files]

        mp3_count = len(count_numbers)
        max_chapter_num = 0
        for root, _, files in os.walk(directory):
            for file in files:

                # 查找文件名中的数字
                numbers = re.findall(r'\d+', file)
                if numbers:
                    max_chapter_num = max(max_chapter_num, max(map(int, numbers)))

            # 同时查找目录名中的数字
            for dir_name in os.listdir(root):
                dir_path = os.path.join(root, dir_name)
                if os.path.isdir(dir_path):
                    numbers = re.findall(r'\d+', dir_name)
                    if numbers:
                        max_chapter_num = max(max_chapter_num, max(map(int, numbers)))
        return mp3_count, max_chapter_num

    def get_folder_mp3_counts(self, base_directory: str) -> List[Dict[str, str]]:
        """
        获取指定目录下的所有文件夹及其MP3文件数量（包含子文件夹中的MP3文件），
        并减去文件名包含"(1)"的部分。解析文件夹名称提取book_id和book_name。

        :param base_directory: 基础目录的路径
        :return: 包含每个文件夹的book_id, book_name, chapter_num的字典列表
        """
        folder_counts = []

        # 获取指定目录下的所有项（文件和文件夹）
        items = os.listdir(base_directory)
        # 筛选出仅包含文件夹的列表
        folders = [item for item in items if os.path.isdir(os.path.join(base_directory, item))]

        for folder in folders:
            folder_path = os.path.join(base_directory, folder)
            book_id, book_name = self.parse_folder_name(folder)
            mp3_count, max_chapter_num = self.get_mp3_count_and_max_chapter(folder_path)
            if mp3_count != max_chapter_num:
                folder_counts.append({
                    "book_id": book_id,
                    "book_name": book_name,
                    "chapter_num": mp3_count,
                    "max_chapter_num": max_chapter_num
                })
            print(f"{folder} 完成统计")
        return folder_counts




    @staticmethod
    def save_to_csv(data: List[Dict[str, str]], output_csv_path: str):
        """
        将数据保存到CSV文件中

        :param data: 包含每个文件夹的book_id, book_name, chapter_num的字典列表
        :param output_csv_path: 输出CSV文件的路径
        """
        df = pd.DataFrame(data)
        df.to_csv(output_csv_path, index=False, encoding='utf-8')

    def set_data(self, df):
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
        grouped['type'] = 2
        grouped['author_name'] = None
        grouped['genre'] = None
        grouped['genre_id'] = None
        grouped['nclass'] = None
        grouped['nclass_id'] = 204
        grouped['book_status'] = None
        grouped['last_update_time'] = None
        grouped['book_num'] = None
        grouped['is_vip'] = None
        grouped['labels'] = None
        grouped['roles'] = None
        grouped['hits'] = None
        grouped['is_daily_recommendation'] = 0
        grouped['is_recommended'] = 0
        grouped['is_highly_rated'] = 0
        grouped['is_reputation'] = 0
        grouped['is_popular'] = 0
        grouped['create_time'] = '2024-04-19 16:43:15'
        grouped['status'] = 1
        grouped['update_time'] = None
        grouped['score'] = None
        grouped['is_featured'] = None


        df.rename(columns={'directory_id': 'book_id', 'new_file_path': 'content'},
                  inplace=True)
        # 添加自增的 chapter_id 列，从 2961 开始
        df['book_id'] = df['book_id'].apply(
            lambda x: self.wash_book_id(x)
        )
        df['content'] = df['content'].apply(
            lambda x: self.wash_content(x)
        )

        df['chapter_id'] = range(2961, 2961 + len(df))

        # 按照 directory_id 分组，为每个组添加从 1 开始的 chapter_num 列
        # df['chapter_num'] = df.groupby('book_id').cumcount() + 1
        df['chapter_num'] = df['content'].apply(lambda x: x.split('-')[-1].split('.')[0].lstrip('0'))
        result = df.to_dict(orient='records')

        df['chapter_vip'] = 0
        df['chapter_name'] = df['chapter_num']
        df['chapter_order'] = df['chapter_num']
        df['last_update_time'] = '2024-03-11 12:00:00'
        df['update_by'] = 1
        df['create_time'] = '2024-03-11 12:00:00'
        df['update_time'] = None

    @staticmethod
    def filter_chapters(input_csv_path: str, output_csv_path: str):
        """
        读取CSV文件并筛选出chapter_num小于max_chapter_num的行，保存到新的CSV文件中。

        :param input_csv_path: 输入的CSV文件路径
        :param output_csv_path: 输出的CSV文件路径
        """
        try:
            # 读取CSV文件
            df = pd.read_csv(input_csv_path)

            # 筛选出chapter_num小于max_chapter_num的行
            filtered_df = df[df['chapter_num'] < df['max_chapter_num']]

            # 将筛选出的行保存到新的CSV文件中
            filtered_df.to_csv(output_csv_path, index=False, encoding='utf-8')
            print(f"Filtered data has been saved to {output_csv_path}")
        except Exception as e:
            print(f"An error occurred: {e}")



def main():
    book_info = BookInfo()
    base_directory_path = r"F:\BaiduNetdiskDownload\【惊雁交音】"  # 将此路径替换为你目标目录的路径
    csv_path = "output.csv"
    filtered_csv_path = "filtered_output.csv"  # 过滤后的CSV文件路径
    result_list = book_info.get_folder_mp3_counts(base_directory_path)
    book_info.save_to_csv(result_list, csv_path)


    # 根据过滤后的book_name列表，对指定目录下的所有ZIP文件进行解压操作
    # folder_counts = book_info.get_folder_mp3_counts(base_directory_path)
    # book_info.filter_chapters(csv_path ,filtered_csv_path)



if __name__ == '__main__':

    main()
