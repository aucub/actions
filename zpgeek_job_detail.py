import os
import json
import re


def sanitize_filename(filename):
    """
    移除或替换不允许的字符
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)


# 读取 JSONL 文件
with open("./export.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        item = json.loads(line)
        job_name = sanitize_filename(item["zpData"]["jobInfo"]["jobName"])
        positionName = (
            sanitize_filename(item["zpData"]["jobInfo"]["positionName"]) or "无分类"
        )
        brand_name = sanitize_filename(item["zpData"]["brandComInfo"]["brandName"])
        directory = os.path.join(
            "zpgeek_job_detail", positionName, job_name, brand_name
        )
        os.makedirs(directory, exist_ok=True)
        # 删除_id字段
        item_id = item["_id"]
        del item["_id"]
        # 生成文件路径
        file_path = os.path.join(directory, f"{item_id}.json")
        # 写入新的 JSON 文件
        with open(file_path, "w", encoding="utf-8") as output_file:
            json.dump(item, output_file, ensure_ascii=False, indent=2)
