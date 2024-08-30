import pandas as pd


def update_file_paths(csv_path, old_directory, new_directory, output_csv_path):
    # 读取CSV文件
    df = pd.read_csv(csv_path, encoding='gbk')

    # 修改file_path列的目录
    df['file_path'] = df['file_path'].str.replace(old_directory, new_directory, regex=False)

    # 保存修改后的CSV文件
    df.to_csv(output_csv_path, index=False)

    return df


# 使用示例
csv_path = 'merged_output_v6.csv'
old_directory = 'F:\\BaiduNetdiskDownload'
new_directory = 'F:\\新短剧'
output_csv_path = 'modified_file.csv'

updated_df = update_file_paths(csv_path, old_directory, new_directory, output_csv_path)
print(updated_df)
