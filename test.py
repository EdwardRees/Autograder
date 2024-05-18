from os import path, system, mkdir, remove, getcwd, chdir
from os.path import isdir
import logging
from util import navigate_to_dir, walk
from clone import test_cloned_check

logger = logging.getLogger()

def read_test_files(assignment_type, assignment_name):
  navigate_to_dir("tests")
  if not isdir(f"{assignment_type}"):
    logger.error(f"{assignment_type} tests missing")
  chdir(f"{assignment_type}")
  if not isdir(f"{assignment_type}-{assignment_name}"):
    logger.error(f"{assignment_type}-{assignment_name} tests missing")
  chdir(f"{assignment_type}-{assignment_name}")


def add_test_to_repo(assignment_type, assignment_name):
  if not test_cloned_check(assignment_type, assignment_name):
    logger.error(f"{assignment_type}-{assignment_name} not cloned!")
    return False

