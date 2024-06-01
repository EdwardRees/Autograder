from os import system, remove, listdir, path, walk, rmdir
from os.path import isdir, sep
from util import walklevel
from shutil import rmtree
import logging

logger = logging.getLogger(__name__)

curr_dir = path.dirname(path.realpath(__file__))


def remove_dir(path):
    if not isdir(path):
        logger.warning("Not a directory")
        return False
    if path == "/":
        logger.warning("Dangerous remove")
        return False
    rmtree(path)
    logger.info(f"Removed {path}")
    return True


def clean(assignment_type, assignment_name):
    if not isdir(f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}"):
        logger.error(f"Assignment {assignment_type}-{assignment_name} not found")
        return
    remove_dir(f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}")

def clean_single(assignment_type, assignment_name, username):
    if not isdir(f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}/{assignment_type}-{assignment_name}-{username}"):
        logger.error(f"Assignment {assignment_type}-{assignment_name}-{username} not found")
        return
    remove_dir(f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}/{assignment_type}-{assignment_name}-{username}")


def clean_tests():
    for root, dirs, files in walklevel("tests"):
        for dir in dirs:
            remove_dir(f"{root}/{dir}")
        for file in files:
            remove(f"{root}/{file}")
    logger.info(f"Removed tests")
