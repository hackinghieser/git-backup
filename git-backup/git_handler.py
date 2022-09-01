"""
Handles Git functions
"""
import subprocess
from progress.bar import Bar

class GitHandler(object):
    """
    Implements different methods
    to handle git repositories
    """
    def __init__(self) -> None:
        pass
    def clone_repo(self,repo:any,token:str,mirror:bool,progress_bar:Bar,destination:str):
        """
        Clone provided repository into
        destination folder
        user full_name for directory name
        """
        repo_fullname = repo['full_name']
        progress_bar.message = f"Clone:{repo_fullname}"
        if mirror:
            subprocess.call(["git", "clone", "--mirror",
                             f"https://{token}@github.com/{repo_fullname}.git",
                             f"{destination}/{repo_fullname}",
                              "--verbose"])
        else:
            subprocess.call(["git", "clone",
                            f"https://{token}@github.com/{repo_fullname}.git",
                            f"{destination}/{repo_fullname}",
                             "--verbose"])

    
