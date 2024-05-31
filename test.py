from os import path, system, mkdir, remove, getcwd, chdir
from os.path import isdir, isfile
import logging
from util import navigate_to_dir, walk
from clone import test_cloned_check, assignment_cloned_check
from shutil import rmtree

curr_dir = path.dirname(path.realpath(__file__))
logger = logging.getLogger(__name__)
# logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s")


def read_test_files(assignment_type, assignment_name):
    navigate_to_dir("tests")
    if not isdir(f"{assignment_type}s"):
        logger.error(f"{assignment_type} tests missing")
    chdir(f"{assignment_type}s")
    if not isdir(f"{assignment_type}-{assignment_name}"):
        logger.error(f"{assignment_type}-{assignment_name} tests missing")
    chdir(f"{assignment_type}-{assignment_name}")
    logger.debug(f"Moved to {getcwd()}")
    test_file = ""
    with open("test.py", "r") as f:
        test_file = f.read()
    chdir("../../..")
    logger.debug(f"Moved to {getcwd()}")
    return test_file


def run_test(assignment_type, assignment_name, username):
    chdir(curr_dir)
    chdir(
        f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}/{assignment_type}-{assignment_name}-{username}"
    )
    logger.debug(f"Navigated to {getcwd()}")

    system("python3 test.py &> result.txt")
    rmtree("__pycache__")
    logger.debug(f"Tested for {assignment_type}-{assignment_name}-{username}")
    result = ""
    with open("result.txt", "r") as f:
        result = f.read()
    chdir("../../../../")
    logger.debug(f"Navigated to {getcwd()}")
    return result


def run_tests(assignment_type, assignment_name, student_usernames, plagarism_checks = None): 
    chdir(curr_dir)
    results = {}
    for username in student_usernames:
        try:
            result = run_test(assignment_type, assignment_name, username)
            logger.debug(
                f"Finished testing {assignment_type}-{assignment_name}-{username}"
            )
            results[username] = result
        except FileNotFoundError:
            logger.warning(f"Failed with {username}")
            results[username] = f"Failed with {username}"
    chdir(f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}")
    with open("results.txt", "w") as f:
        for name, result in results.items():
            """
            If plagarism_checks is not None, check if the name is in the check pairs. If it is, add an additional f.write between the name and result that contains "FLAGGED FOR PLAGIARISM"
            """
            f.write(f"{name}")
            if plagarism_checks is not None and name in plagarism_checks:
                f.write(f" [FLAGGED FOR PLAGIARISM]\n\n")
                f.write("Check with the following students:\n")
                for group in plagarism_checks.get(name):
                    for paired_name, score in group.items():
                        f.write(f"\t- {name} with {paired_name}. Similarity score: {score}\n")

            f.write("\n")
            f.write(f"{result}\n\n")
            f.write("-" * 40)
            f.write("\n\n\n")
        f.write("\n")
    logger.debug(f"Written out to {getcwd()}/results.txt")
    chdir(f"../../")


def add_test_to_repo(assignment_type, assignment_name, usernames):
    if not test_cloned_check(assignment_type, assignment_name):
        logger.error(f"{assignment_type}-{assignment_name} tests not cloned!")
        return False
    if not assignment_cloned_check(assignment_type, assignment_name):
        logger.error(f"{assignment_type}-{assignment_name} assignment not cloned!")
        return False
    test_file = read_test_files(assignment_type, assignment_name)
    for root, _, _ in walk(
        f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}"
    ):
        if "__pycache__" in root:
            continue
        actual = root.split("/")[-1]
        if actual == f"{assignment_type}-{assignment_name}":
            continue
        if "-".join(actual.split("-")[2:]) in usernames:
            chdir(root)
            with open("test.py", "w") as f:
                f.write(test_file)
            logger.debug(f"Test file written out to {getcwd()}")
            chdir("../../../..")
            logger.debug(f"Navigated back to {getcwd()}")
