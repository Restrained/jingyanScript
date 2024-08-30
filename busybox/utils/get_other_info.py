import pandas as pd
import re

def clean_parent_directory(name):
    match = re.search(r'《(.*?)》', name)
    if match:
        name = match.group(1)
    # 删除空格、.、-和_
    name = re.split(r'[ .\-_（]', name)[0]
    # 删除 "全集"、"成片"、"修改版" 和 数字+集
    name = re.sub(r'(全集|成片|修改版|\d+集|无水印版|1007|海报\+)', '', name)

    name = name.replace('，', ' ')
    name = name.replace('村民沈风致富路', '无双神医')
    name = name.replace('九龙战神', '九神战龙')
    name = name.replace('九龙战神', '九神战龙')
    name = name.replace('极品医仙', '极品武道医仙')
    if '心死后' in name:
        print(111)
    return name

# 读取两个CSV文件
original_csv = "file_info.csv"  # 原CSV文件路径
second_csv = "alias.csv"  # 第二个CSV文件路径

df_original = pd.read_csv(original_csv)
df_second = pd.read_excel('短剧2.xlsx')


# 假设第二个CSV文件的剧名列名为'drama_name'，封面名字列为'cover_name'，简介列为'description'
drama_name_col = 'origin_name'
cover_name_col = 'new_name'
description_col = 'intro'

# 初始化封面名字及简介列
df_original[cover_name_col] = ""
df_original[description_col] = ""

df_original['clean_parent_directory'] = df_original['parent_directory'].apply(clean_parent_directory)

# 遍历原CSV文件的每一行，并进行匹配
for index, row in df_original.iterrows():
    parent_directory = row['clean_parent_directory']
    matching_rows = df_second[df_second[drama_name_col].str.contains(parent_directory, na=False)]

    if not matching_rows.empty:

        origin_name = matching_rows[drama_name_col].values[0]
        cover_name = matching_rows[cover_name_col].values[0]
        description = matching_rows[description_col].values[0]

        df_original.at[index, drama_name_col] = origin_name
        df_original.at[index, cover_name_col] = cover_name
        df_original.at[index, description_col] = description

# 保存合并后的结果到新CSV文件
output_csv = "merged_output_v6.csv"  # 新CSV文件路径
df_original.to_csv(output_csv, index=False)

print(f"合并后的CSV文件已保存到: {output_csv}")
