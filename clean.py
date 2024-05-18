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
    logger.info(f"Assignment {assignment_type}-{assignment_name} not found")
    return
  remove_dir(f"assignments/{assignment_type}s/{assignment_type}-{assignment_name}")

if __name__ == "__main__":
  remove_dir("assignments/hello")
