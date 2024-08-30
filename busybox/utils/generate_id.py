import os
import csv
import re


def generate_file_info(directory_list):
    file_info_list = []
    starting_id = 32

    for directory in directory_list:
        directory_id = starting_id
        found_mp4 = False

        # 检查给定目录下是否有 MP4 文件
        for file in os.listdir(directory):
            if file.endswith(".mp4"):
                found_mp4 = True
                break

        if found_mp4:
            # 处理给定目录下的 MP4 文件
            for file in os.listdir(directory):
                if file.endswith(".mp4"):
                    file_path = os.path.join(directory, file)
                    file_name = os.path.splitext(file)[0]
                    if file_name.isdigit():
                        file_id = file_name.zfill(3)
                        combined_id = f"{directory_id}-{file_id}"
                        parent_directory = directory.split("\\")[-1]
                        file_info_list.append({
                            "file_path": file_path,
                            "parent_directory": parent_directory,
                            "generated_id": combined_id,
                            "directory_id": directory_id
                        })
            starting_id += 1
        else:
            # 处理子目录中的 MP4 文件
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".mp4"):
                        found_mp4 = True
                        file_path = os.path.join(root, file)
                        file_name = os.path.splitext(file)[0]
                        if file_name.isdigit():
                            file_id = file_name.zfill(3)
                            combined_id = f"{directory_id}-{file_id}"
                            parent_directory = directory.split("\\")[-1]
                            file_info_list.append({
                                "file_path": file_path,
                                "parent_directory": parent_directory,
                                "generated_id": combined_id,
                                "directory_id": directory_id
                            })
                if found_mp4:
                    break
            starting_id += 1

    return file_info_list

def save_to_csv(file_info_list, csv_filename):
    fieldnames = ["file_path", "parent_directory", "generated_id", "directory_id"]
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for file_info in file_info_list:
            writer.writerow(file_info)


def rename_mov_to_mp4(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.mov'):
                mov_file_path = os.path.join(root, file_name)
                mp4_file_path = os.path.join(root, os.path.splitext(file_name)[0] + '.mp4')

                os.rename(mov_file_path, mp4_file_path)
                print(f"Renamed {mov_file_path} to {mp4_file_path}")





def remove_prefix(directory, prefix):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.mp4'):
                new_file_name = file_name
                if file_name.startswith(prefix):
                    new_file_name = re.sub(r'^' + prefix, '', file_name)
                mp4_file_path = os.path.join(root, file_name)
                new_mp4_file_path = os.path.join(root, new_file_name)

                if mp4_file_path != new_mp4_file_path:
                    os.rename(mp4_file_path, new_mp4_file_path)
                    print(f"Renamed {mp4_file_path} to {new_mp4_file_path}")
# 示例使用
directory_list = [
    r"F:\BaiduNetdiskDownload\独断万古 诸君且听龙吟",
    r"F:\BaiduNetdiskDownload\九龙战神全集-成片",
    r"F:\BaiduNetdiskDownload\我的女友是狐仙全集",
    r"F:\BaiduNetdiskDownload\【物料】娇妻无罪（封面+海报+照片）",
    r"F:\BaiduNetdiskDownload\天降巨富-封面",
    r"F:\BaiduNetdiskDownload\总裁前任跪地求复合 剧照、图片",
    r"F:\BaiduNetdiskDownload\尊上归来-成片",
    r"F:\BaiduNetdiskDownload\我在横店当大仙72集",
    r"F:\BaiduNetdiskDownload\极品义子成片",
    r"F:\BaiduNetdiskDownload\赤焰神瞳成片1007",
    r"F:\BaiduNetdiskDownload\总裁的亿万囚妻-成片",
    r"F:\BaiduNetdiskDownload\女首富的复仇",
    r"F:\BaiduNetdiskDownload\娇妻不知足",
    r"F:\BaiduNetdiskDownload\昆仑强者成片",
    r"F:\BaiduNetdiskDownload\极品医仙",
    r"F:\BaiduNetdiskDownload\囚龙岛全集",
    r"F:\BaiduNetdiskDownload\绝命洗屋人",
    r"F:\BaiduNetdiskDownload\毒手赘婿修改版",
    r"F:\BaiduNetdiskDownload\偏执陆总求放过.高清成片最新",
    r"F:\BaiduNetdiskDownload\祁少他入戏太深成片无水印版",
    r"F:\BaiduNetdiskDownload\五万存款当首富",
    r"F:\BaiduNetdiskDownload\村民沈风致富路",
    r"F:\BaiduNetdiskDownload\极品长生大天师（全集100）",
    r"F:\BaiduNetdiskDownload\极品龙王",
    r"F:\BaiduNetdiskDownload\心死后，渣男前夫追悔莫及",
    r"F:\BaiduNetdiskDownload\《富甲天下》定稿版",
    r"F:\BaiduNetdiskDownload\天命娇妻_成片mov",
    r"F:\BaiduNetdiskDownload\绝世股神 精剪",
    r"F:\BaiduNetdiskDownload\我的渣夫柳先生海报+成片",
    r"F:\BaiduNetdiskDownload\狂飙1990 成品字幕版87集",
    r"F:\BaiduNetdiskDownload\重生狂医",
    r"F:\BaiduNetdiskDownload\逍遥皇太子  重生之我爹是皇帝",
    r"F:\BaiduNetdiskDownload\命有乾坤  绝命风水师"
]

if __name__ == "__main__":
    # for file_path in directory_list:
    #     rename_mov_to_mp4(file_path)

    # for file_path in directory_list:
    #     remove_chinese_from_mp4(file_path)

    file_info = generate_file_info(directory_list)
    csv_filename = 'file_info.csv'
    save_to_csv(file_info, csv_filename)

    # directory = r"F:\BaiduNetdiskDownload\狂飙1990 成品字幕版87集"
    # prefix = "1990"
    # remove_prefix(directory, prefix)