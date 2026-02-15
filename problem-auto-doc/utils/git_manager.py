import subprocess
import os

def check_git_connection():
    """
    Checks if git is initialized in the parent directory and has a remote origin.
    This is designed for structures where the .git folder is one level above the script.
    """
    try:
        # Executes 'git remote -v' in the parent directory using the -C flag
        result = subprocess.run(["git", "-C", "..", "remote", "-v"], capture_output=True, text=True)
        # Returns True if 'origin' is found in the remote list of the parent directory
        return result.returncode == 0 and "origin" in result.stdout
    except:
        return False

def git_commit_and_push(day_num, problem_title):
    """
    Performs git add, commit, and push operations targeting the parent repository.
    """
    try:
        commit_message = f"Add Day {day_num:04d}: {problem_title}"
        
        # Uses '-C ..' to tell Git to operate on the parent directory (the root of your repo)
        # Adds all changes in the parent repository
        subprocess.run(["git", "-C", "..", "add", "."], check=True)
        
        # Commits the changes with a formatted message
        subprocess.run(["git", "-C", "..", "commit", "-m", commit_message], check=True)
        
        # Pushes the local commits to the remote repository
        subprocess.run(["git", "-C", "..", "push"], check=True)
        return True
    except Exception as e:
        print(f"❌ Git Error: {e}")
        return False
