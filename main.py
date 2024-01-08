from os import getenv

from github import Github as gh
from requests import get

auth_token = getenv("AUTH_TOKEN")
git_repo = getenv("GIT_REPO")
commit_msg = getenv("COMMIT_MSG")
username = getenv("USERNAME")

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": "bearer " + auth_token,
}

g = gh(auth=auth_token)

START_AT = getenv("START_AT")
END_AT = getenv("END_AT")


def get_default_branch(f_repo):
    """

    :param f_repo:

    """
    api_url = f"https://api.github.com/repos/{f_repo}"

    response = get(api_url, headers=headers)

    if response.status_code == 200:
        default_branch = response.json()["default_branch"]
        return default_branch
    else:
        return None


def calculate_language_size(f_repo):
    """

    :param f_repo:

    """
    for repo in g.get_user().get_repos():
        data = f"https://api.github.com/repos/{repo}/languages"
        return data


def push_to_repo(f_path, f_repo, d_branch, c_msg, content):
    """

    :param f_path:
    :param f_repo:
    :param d_branch:
    :param c_msg:
    :param content:

    """
    try:
        repo = g.get_repo(f_repo)
        contents = repo.get_contents(f_path, ref=d_branch)

        repo.update_file(
            branch=d_branch,
            path=contents.path,
            sha=contents.sha,
            message=c_msg,
            content=content,
        )

        print(
            f"Successfully pushed to {d_branch} branch in {f_repo} repository."
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    repo = g.get_repo(git_repo)
    f_path = repo.get_readme()
    d_branch = get_default_branch(git_repo)

    # Since most branches moved to "main" then use it incase
    if d_branch is None:
        d_branch = "main"
    c_msg = commit_msg
    content = calculate_language_size(git_repo)
    push_to_repo(f_path, git_repo, d_branch, c_msg, content)
