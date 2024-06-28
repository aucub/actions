import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# GitHub 个人访问令牌
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
# GitHub 用户名
GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
# 仓库名称，格式为 "owner/repo"
github_repo_list = [
    "aucub/actions",
    "aucub/nix-config",
    "aucub/tasteless",
    "aucub/aucub",
    "aucub/WindowsPE",
    "aucub/build-nixos-iso",
    "aucub/ampg",
]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def delete_workflow_runs(repo):
    error_count = 0
    while error_count < 3:
        # 获取 Workflow 运行记录
        url = f"https://api.github.com/repos/{repo}/actions/runs"
        response = httpx.get(url, headers=headers)
        runs = response.json().get("workflow_runs", [])
        if len(runs) == 0:
            break
        for run in runs:
            run_id = run["id"]
            delete_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}"
            delete_response = httpx.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print(f"Successfully deleted run {run_id}")
            else:
                print(
                    f"Failed to delete run {run_id}, status code {delete_response.status_code}"
                )
                error_count = error_count + 1


if __name__ == "__main__":
    for github_repo in github_repo_list:
        delete_workflow_runs(github_repo)
