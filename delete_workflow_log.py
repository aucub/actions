import requests

# GitHub 个人访问令牌
TOKEN = ""
# GitHub 用户名
USERNAME = ""
# 仓库名称，格式为 "owner/repo"
REPO = ""

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def delete_workflow_runs(repo):
    while True:
        # 获取 Workflow 运行记录
        url = f"https://api.github.com/repos/{repo}/actions/runs"
        response = requests.get(url, headers=headers)
        runs = response.json().get("workflow_runs", [])
        if len(runs) == 0:
            break
        for run in runs:
            run_id = run["id"]
            delete_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print(f"Successfully deleted run {run_id}")
            else:
                print(
                    f"Failed to delete run {run_id}, status code {delete_response.status_code}"
                )


if __name__ == "__main__":
    delete_workflow_runs(REPO)
