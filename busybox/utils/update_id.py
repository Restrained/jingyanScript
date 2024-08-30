import pandas as pd


def update_directory_id(csv_path, output_csv_path):
    # 读取CSV文件
    df = pd.read_csv(csv_path)

    # 确保'directory_id'列存在
    if 'directory_id' not in df.columns:
        raise ValueError("The CSV file does not contain a 'directory_id' column.")

    # 将'directory_id'列中的值加1
    df['directory_id'] = df['directory_id'] + 1

    # 保存到新的CSV文件
    df.to_csv(output_csv_path, index=False)
    print(f"Updated CSV saved to {output_csv_path}")


# 使用示例
csv_path = 'modified_file.csv'  # 替换为你的输入CSV文件路径
output_csv_path = 'updated_directory_id.csv'  # 替换为你想要保存的输出文件路径

update_directory_id(csv_path, output_csv_path)
