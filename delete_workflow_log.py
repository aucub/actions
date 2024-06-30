import os
import requests
from dotenv import load_dotenv

load_dotenv()

# GitHub 个人访问令牌
github_token = os.environ["GITHUB_TOKEN"]
# GitHub 用户名
github_username = os.environ["GITHUB_USERNAME"]
# 仓库名称
github_repo_list = [
    "actions",
    "nix-config",
    "tasteless",
    "WindowsPE",
    "build-nixos-iso",
    "ampg",
]

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}


def delete_workflow_runs(repo):
    error_count = 0
    while error_count < 3:
        # 获取 Workflow 运行记录
        url = f"https://api.github.com/repos/{repo}/actions/runs?status=completed"
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
                error_count = error_count + 1


if __name__ == "__main__":
    for github_repo in github_repo_list:
        delete_workflow_runs(github_username + "/" + github_repo)
