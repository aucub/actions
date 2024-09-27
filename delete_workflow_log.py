import os
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

# GitHub 个人访问令牌
github_token = os.environ["GITHUB_TOKEN"]
# GitHub 用户名
github_username = os.environ["GITHUB_USERNAME"]
# 仓库名称列表
github_repo_list = [
    "actions",
    "nix-config",
    "build-nixos-iso",
]

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}


def delete_workflow_runs(repo):
    error_count = 0
    while error_count < 3:
        url = f"https://api.github.com/repos/{repo}/actions/runs?status=completed"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(
                f"Failed to fetch workflow runs for {repo}, status code {response.status_code}"
            )
            error_count += 1
            continue

        runs = response.json().get("workflow_runs", [])
        if len(runs) == 0:
            break

        for run in runs:
            run_id = run["id"]
            delete_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print(f"Successfully deleted run {run_id} from {repo}")
            else:
                print(
                    f"Failed to delete run {run_id} from {repo}, status code {delete_response.status_code}"
                )
                error_count += 1
        if error_count >= 3:
            print(f"Error limit reached for {repo}, stopping deletions.")
            break


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(delete_workflow_runs, github_username + "/" + repo)
            for repo in github_repo_list
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")
