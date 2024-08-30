import pandas as pd
import os
import shutil
from loguru import logger


def process_files(csv_path, output_directory, new_csv_path):
    index = 0
    # 设置日志格式
    logger.add("file_process.log", format="{time} {level} {message}", level="INFO")

    # 读取CSV文件
    df = pd.read_csv(csv_path)

    # 创建输出目录（如果不存在）
    os.makedirs(output_directory, exist_ok=True)

    new_paths = []

    for _, row in df.iterrows():
        file_path = row['file_path']
        directory_id = row['directory_id']

        # 获取文件名和扩展名
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)

        # 构建新文件名和新路径
        new_file_name = f"{directory_id}-{name}{ext}"
        new_file_path = os.path.join(output_directory, new_file_name)

        # 检查文件是否已存在
        if os.path.exists(  ):
            logger.info(f"File {index + 1}: {new_file_path} already exists. Skipping.")
            new_paths.append(new_file_path)
            continue

        # 复制并重命名文件
        shutil.copy2(file_path, new_file_path)

        # 记录新路径
        new_paths.append(new_file_path)

        # 打印日志信息
        logger.info(f"{index + 1}Copied and renamed file from {file_path} to {new_file_path}")
        index += 1
    # 将新路径添加到原DataFrame
    df['new_file_path'] = new_paths

    # 保存新的CSV文件
    df.to_csv(new_csv_path, index=False)

    logger.info(f"Process completed. New CSV saved to {new_csv_path}")

    return df


# 使用示例
csv_path = 'updated_directory_id.csv'
output_directory = 'F:\\movie_output'
new_csv_path = 'new_file_paths.csv'

result_df = process_files(csv_path, output_directory, new_csv_path)
print(result_df)
