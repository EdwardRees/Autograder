from os import path, system, mkdir, remove, getcwd, chdir
from os.path import isdir
import logging
from util import navigate_to_dir, walk
from clone import test_cloned_check, assignment_cloned_check

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
  with open("test.py", 'r') as f:
    test_file = f.read()
  chdir("../../..")
  logger.debug(f"Moved to {getcwd()}")
  return test_file

def run_test(assignment_type, assignment_name, username):
  # TODO Run the test for an individual student 
  pass

def add_test_to_repo(assignment_type, assignment_name):
  if not test_cloned_check(assignment_type, assignment_name):
    logger.error(f"{assignment_type}-{assignment_name} tests not cloned!")
    return False
  if not assignment_cloned_check(assignment_type, assignment_name):
    logger.error(f"{assignment_type}-{assignment_name} assignment not cloned!")
    return False
  test_file = read_test_files(assignment_type, assignment_name)
  for root, _, _ in walk(f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}"):
    actual = root.split("/")[-1]
    if actual == f"{assignment_type}-{assignment_name}":
      continue
    chdir(root)
    with open("test.py", 'w') as f:
      f.write(test_file)
    logger.debug(f"Test file written out to {getcwd()}")
    chdir("../../../..")
    logger.debug(f"Navigated back to {getcwd()}")

