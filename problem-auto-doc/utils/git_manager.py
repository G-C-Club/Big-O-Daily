import subprocess
import os

def check_git_connection():
    """Checks if git is initialized and has a remote origin."""
    try:
        # Check if it's a git repo and has a remote
        result = subprocess.run(["git", "remote", "v"], capture_output=True, text=True)
        return result.returncode == 0 and "origin" in result.stdout
    except:
        return False

def git_commit_and_push(day_num, problem_title):
    """Performs git add, commit, and push."""
    try:
        commit_message = f"Add Day {day_num:04d}: {problem_title}"
        
        # We assume the 'problems' folder is one level up
        subprocess.run(["git", "add", ".."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except Exception as e:
        print(f"❌ Git Error: {e}")
        return False
