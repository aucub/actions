import os
import json


# 读取 JSONL 文件
with open("./export.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        item = json.loads(line)
        if not item["zpData"]["jobList"]:
            continue
        directory = os.path.join("zpgeek_job_joblist", item["zpData"]["lid"])
        os.makedirs(directory, exist_ok=True)
        # 删除_id字段
        item_id = item["_id"]["$oid"]
        del item["_id"]
        # 生成文件路径
        file_path = os.path.join(directory, f"{item_id}.json")
        # 写入新的 JSON 文件
        with open(file_path, "w", encoding="utf-8") as output_file:
            json.dump(item, output_file, ensure_ascii=False, indent=2)
