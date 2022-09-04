"""
GitBackup script
"""
import argparse
import json
from shutil import which
import requests
from progress.bar import Bar
from gitbackup.githandler import GitHandler

def check_git():
    """Check if 'GIT' is in path"""
    return which('git') is not None

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
                                     headers={'Authorization': str(
                                         "token "+token)},
                                     timeout=2000,
                                     params={'page': page, 'per_page': 100})
        if private_repos.json() == []:
            paging = False
        repos = repos + private_repos.json()
        page = page + 1
    return repos


def clone_repositories(git=GitHandler,
                       destination=str,
                       username=str,
                       access_token=str,
                       mirror=bool):
    """
    Clone repositories from user
    into the destination path
    """
    repositories = get_repositoires(access_token)
    print(str("\n ## Repositories found (private,public and invitations): " +
          json.dumps(len(repositories))) + " ## \n")
    if username != "":
        print(f"Filter for Username: {username}")

    with Bar('Clong repositories', max=len(repositories),
             suffix='%(remaining)d of %(max)d repositories left...') as progress_bar:
        for repo in repositories:
            if username != "":
                if repo["owner"]["login"] == username:
                    git.clone_repo(repo=repo,
                                   token=access_token,
                                   mirror=mirror,
                                   progress_bar=progress_bar,
                                   destination=destination)
                    progress_bar.next()
            else:
                git.clone_repo(repo=repo,
                               token=access_token,
                               mirror=mirror,
                               progress_bar=progress_bar,
                               destination=destination)
                progress_bar.next()


def run_cli():
    '''Execute clis tartup'''
    print(" @@@@@@@  @@@ @@@@@@@ @@@@@@@   @@@@@@   @@@@@@@ @@@  @@@ @@@  @@@ @@@@@@@ \n" +
          "!@@       @@!   @!!   @@!  @@@ @@!  @@@ !@@      @@!  !@@ @@!  @@@ @@!  @@@ \n" +
          "!@! @!@!@ !!@   @!!   @!@!@!@  @!@!@!@! !@!      @!@@!@!  @!@  !@! @!@@!@! \n" +
          ":!!   !!: !!:   !!:   !!:  !!! !!:  !!! :!!      !!: :!!  !!:  !!! !!: \n" +
          " :: :: :  :      :    :: : ::   :   : :  :: :: :  :   :::  :.:: :   :     \n \n ")

    # Check if git is installed
    if check_git() is True:
        # Setup CLI arguments
        parser = argparse.ArgumentParser(description='Welcome, use cmd line arguments ' +
                                        'or wizard to create your remote backups.')
        parser.add_argument('-t', type=str, required=True, dest="access_token",
                            help='Your Github API Access Token')
        parser.add_argument('-p', type=str, dest="destination",
                            help='Backup destination path')
        parser.add_argument('-u', type=str, dest="username",
                            help='Username')
        parser.add_argument('--mirror', action="store_true",
                            dest="mirror", help="Git Mirror repositories")
        args = parser.parse_args()
        access_token = args.access_token or ""
        destination = args.destination or "."
        username = args.username or ""
        mirror = args.mirror
        git = GitHandler()
        clone_repositories(git=git, username=username, destination=destination,
                        mirror=mirror, access_token=access_token)
    else:
        print('GIT not found in path. Please install git and retry.')
        exit()
