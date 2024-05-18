from os import system, mkdir, remove, getcwd, chdir
from os.path import isdir
import logging

logger = logging.getLogger(__name__)

def generate_assignment_link(course_name, assignment_type, assignment_name, username):
    return f"git@github.com:{course_name}/{assignment_type}-{assignment_name}-{username}"

def nav_to_assignments():
    pwd = getcwd().split("/")
    if "autograder" == pwd[-1]:
        chdir("assignments")
        return getcwd().split("/")
    if pwd[-2:] != ['autograder', 'assignments']:
        assignment_idx = pwd.index("assignments")
        backtracks = len(pwd) - assignment_idx
        for _ in range(backtracks):
            chdir("..")
    logger.debug(f"Navigated to {getcwd()}")
    return getcwd().split("/")

def get_username(names, name):
    for (student_name, username) in names.items():
        if student_name == name:
            logger.debug(f"Found {name} with username: {username}")
            return username
    logger.warning(f"No username with name {name} found")
    return None

def clone_assignment(course_name, assignment_type, assignment_name, username):
    if assignment_type not in ['project', 'lab', 'inclass']:
        logger.info(f"Invalid assignment type: {assignment_type}")
        return
    dir_name = f"{assignment_type}-{assignment_name}-{username}"
    if isdir(dir_name):
        system(f"rm {dir_name}")
    url = generate_assignment_link(course_name, assignment_type, assignment_name, username)

    system(f"git clone {url}")
    chdir(dir_name)
    logger.debug(f"Cloned {dir_name}")
    system("rm -rf .git")
    logger.debug(f"Removed .git folder")
    chdir("..")
    logger.debug(f"Returned to {getcwd()}")

def clone(course_name, assignment_type, assignment_name, student_usernames):
    if assignment_type not in ["project", "lab", "inclass"]:
        print("Invalid assignment type")
        return
    chdir("assignments")
    if not isdir(f"{assignment_type}s"):
        mkdir(f"{assignment_type}s")
    chdir(f"{assignment_type}s")
    if not isdir(f"{assignment_type}-{assignment_name}"):
        mkdir(f"{assignment_type}-{assignment_name}")
    chdir(f"{assignment_type}-{assignment_name}")
    cloned_repos = {"successful": [], "unsuccessful": []}
    for username in student_usernames:
        try:
            clone_assignment(course_name, assignment_type, assignment_name, username)
            cloned_repos.get("successful").append(username)
        except FileNotFoundError:
            cloned_repos.get("unsuccessful").append(username)
            continue
    chdir("../..")
    logger.debug(f"Successfully cloned: {cloned_repos.get('successful')}")
    logger.debug(f"Failed to clone: {cloned_repos.get('unsuccessful')}")
    logger.debug(f"Navigated back to {getcwd()}")

