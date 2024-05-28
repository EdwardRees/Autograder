import logging
from os import system, mkdir, remove, getcwd, chdir, path
from os.path import isdir
from util import navigate_to_dir
from clean import remove_dir

logger = logging.getLogger(__name__)
curr_dir = path.dirname(path.realpath(__file__))

def generate_assignment_link(course_name, assignment_type, assignment_name, username):
    return f"git@github.com:{course_name}/{assignment_type}-{assignment_name}-{username}"

def nav_to_assignments():
    return navigate_to_dir("assignments")

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
        remove_dir(f"{dir_name}")
        logger.info(f"Directory already exists, removed {dir_name}")
    url = generate_assignment_link(course_name, assignment_type, assignment_name, username)

    system(f"git clone {url}")
    chdir(dir_name)
    logger.debug(f"Cloned {dir_name}")
    remove_dir(".git")
    logger.debug(f"Removed .git folder")
    chdir("..")
    logger.debug(f"Returned to {getcwd()}")
    return

def clone(course_name, assignment_type, assignment_name, student_usernames):
    if assignment_type not in ["project", "lab", "inclass"]:
        print("Invalid assignment type")
        return
    if not isdir("assignments"):
        mkdir("assignments")
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
    return

def test_cloned_check(assignment_type, assignment_name):
  assignment_string = f"{assignment_type}-{assignment_name}"
  logger.debug(f"Checking {curr_dir}/tests/{assignment_type}s/{assignment_string}")
  return isdir(f"{curr_dir}/tests/{assignment_type}s/{assignment_string}")

def assignment_cloned_check(assignment_type, assignment_name):
  assignment_string = f"{assignment_type}-{assignment_name}"
  logger.debug(f"Checking {curr_dir}/assignment/{assignment_type}s/{assignment_string}")
  return isdir(f"{curr_dir}/assignments/{assignment_type}s/{assignment_string}")


def clone_tests(test_repo):
  if not isdir("tests"):
    mkdir("tests")
  navigate_to_dir("tests")
  system(f"git clone --depth 1 {test_repo} . ")
  logger.info(f"Cloned test repos into tests folder")
  return True


def pull_tests():
  navigate_to_dir("tests")
  system("git pull")
  logger.info(f"Pulled newest tests")
  return True

