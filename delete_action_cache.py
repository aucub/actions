import os
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

# GitHub 个人访问令牌
github_token = os.environ["GITHUB_TOKEN"]
# GitHub 用户名
github_username = os.environ["GITHUB_USERNAME"]
# 仓库名称
github_repo_list = [
    "nix-config",
]

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}


def delete_cache(repo, cache_id):
    delete_url = f"https://api.github.com/repos/{repo}/actions/caches/{cache_id}"
    delete_response = requests.delete(delete_url, headers=headers)
    if delete_response.status_code == 204:
        print(f"Successfully deleted cache {cache_id}")
    else:
        print(
            f"Failed to delete cache {cache_id}, status code {delete_response.status_code}"
        )
    return delete_response.status_code == 204


def delete_workflow_runs(repo):
    error_count = 0
    while error_count < 3:
        url = f"https://api.github.com/repos/{repo}/actions/caches"
        response = requests.get(url, headers=headers)
        caches = response.json().get("actions_caches", [])
        if len(caches) == 0:
            break

        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(delete_cache, repo, cache["id"]): cache["id"]
                for cache in caches
            }
            for future in as_completed(futures):
                cache_id = futures[future]
                try:
                    success = future.result()
                    if not success:
                        error_count += 1
                        if error_count >= 3:
                            print(
                                f"Failed too many times on cache {cache_id}, aborting."
                            )
                            break
                except Exception as exc:
                    print(f"Cache {cache_id} generated an exception: {exc}")
                    error_count += 1
                    if error_count >= 3:
                        break


if __name__ == "__main__":
    for github_repo in github_repo_list:
        delete_workflow_runs(github_username + "/" + github_repo)
