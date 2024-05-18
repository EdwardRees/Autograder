from os import path
from os.path import isdir
import logging

logger = logging.getLogger()
curr_dir = path.dirname(path.realpath(__file__))

def test_cloned_check(assignment_type, assignment_name):
  assignment_string = f"{assignment_type}-{assignment_name}"
  logger.debug(f"Checking {curr_dir}/tests/{assignment_type}/{assignment_string}")
  return isdir(f"{curr_dir}/tests/{assignment_type}/{assignment_string}")

if __name__ == "__main__":
  print(test_cloned_check("project", "1"))

