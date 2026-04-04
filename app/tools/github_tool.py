import requests
import os

def get_github_issues(repo):
    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    issues = []
    for issue in data[:5]:
        issues.append({
            "title": issue.get("title"),
            "state": issue.get("state")
        })

    return issues