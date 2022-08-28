"""
GitBackup script
"""
import argparse
import json
import requests
from progress.bar import Bar
from git_handler import GitHandler


# Setup CLI arguments

parser = argparse.ArgumentParser(description='Git Backup, running')
parser.add_argument('-t',type=str, required=True, dest="access_token",
                    help='Your Github API Access Token')
parser.add_argument('-p',type=str, dest="destination",
                    help='Backup destination path')
parser.add_argument('--mirror', action="store_true", dest="mirror", help="Git Mirror repositories")
args = parser.parse_args()
# Init Attributes
ACCESS_TOKEN = args.access_token or ""
DESTINATION = args.destination or "."
mirror = args.mirror

git = GitHandler()

def get_repositoires(token=str):
    """
    Get all repositories from
    user with access token
    """
    paging = True
    page = 1
    repos = json.loads("[]")
    while paging:
        private_repos = requests.get('https://api.github.com/user/repos',
         headers={'Authorization':str("token "+token)},
         timeout=2000,
         params={'page':page, 'per_page': 100})
        if private_repos.json() == []:
            paging = False
        repos  = repos + private_repos.json()
        page = page + 1
    return repos

def clone_repositories():
    """
    Clone repositories from user
    into the destination path
    """
    repositories = get_repositoires(args.access_token)
    print(str("\n ## Repositories found: "+json.dumps(len(repositories)))+ " ## \n")
    with Bar('Clong repositories', max=len(repositories),
        suffix='%(remaining)d of %(max)d repositories left...') as progress_bar:
        for repo in repositories:
            git.clone_repo(repo=repo,
                            token=ACCESS_TOKEN,
                            mirror=mirror,
                            progress_bar=progress_bar,
                            destination=DESTINATION)
            progress_bar.next()



#Execute Git Backup script
if __name__ == "__main__":
    clone_repositories()
else:
    print("Done \n")
