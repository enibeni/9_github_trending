import requests
import json
import datetime
import sys


def get_trending_repositories(top_size):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    request_params = {
        "q": "created:>{}".format(week_ago),
        "sort": "stars",
        "order": "desc",
        'per_page': top_size,
    }
    response = requests.get(
        "https://api.github.com/search/repositories",
        params=request_params
    )
    if response.ok:
        trending_repos = json.loads(response.content)["items"]
        return trending_repos
    else:
        return None


def get_open_issues_amount(repo):
    repo_name = repo["full_name"]
    response = requests.get(
        "https://api.github.com/repos/{repo_name}/issues".format(
            repo_name=repo_name
        )
    )
    if response.ok:
        open_issues = json.loads(response.content)
        return len(open_issues)
    else:
        return None


def print_repo_info(repo):
    print("Name:{full_name} *:{stars}".format(
        full_name=repo["full_name"],
        stars=repo["stargazers_count"]
        )
    )
    print("{}".format(repo["html_url"]))


def print_issues_amount(open_issues_amount):
    if open_issues_amount is None:
        print("Ошибка в запросе получения списка issues\n")
    else:
        print("Колличество открытых issues:{}\n".format(open_issues_amount))


if __name__ == "__main__":
    top_size_of_repos = 20
    trending_repos = get_trending_repositories(top_size_of_repos)
    if trending_repos is None:
        sys.exit("Ошибка в запросе")
    else:
        for repo in trending_repos:
            print_repo_info(repo)
            open_issues_amount = get_open_issues_amount(repo)
            print_issues_amount(open_issues_amount)
