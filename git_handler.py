from asyncio.subprocess import STDOUT
import subprocess
from progress.bar import Bar

"""
Implements different methods
to handle git repositories
"""
class git_handler:
    """
    Clone provided repository into
    destination folder
    user full_name for directory name
    """
    def cloneRepo(self,repo:any,token:str,mirror:bool,bar:Bar,destination:str):
        repo_fullname = repo['full_name']
        bar.message = f"Clone:{repo_fullname}"
        if mirror:
            subprocess.call(["git", "clone", "--mirror", f"https://{token}@github.com/"+ repo_fullname +".git",f"{destination}/{repo_fullname}", "--verbose"], stdout=subprocess.DEVNULL, stderr=STDOUT)
        else:
            subprocess.call(["git", "clone", f"https://{token}@github.com/"+ repo_fullname +".git",f"{destination}/{repo_fullname}", "--verbose"], stdout=subprocess.DEVNULL, stderr=STDOUT)
