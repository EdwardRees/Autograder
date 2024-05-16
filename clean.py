from os import system, remove, listdir, path, walk, rmdir
from os.path import isdir, sep
from util import walklevel
from shutil import rmtree

curr_dir = path.dirname(path.realpath(__file__))

def remove_dir(path):
  if not isdir(path):
    print("Not a directory")
    return False
  if path == "/":
    print("Dangerous remove")
    return False
  rmtree(path)
  print(f"Removed {path}")
  return True

def clean(assignment_type, assignment_name):
  if not isdir(f"assignments/{assignment_type}-{assignment_name}"):
    print(f"Assignment {assignment_type}-{assignment_name} not found")
    return
  remove_dir(f"assignments/{assignment_type}-{assignment_name}")

if __name__ == "__main__":
  remove_dir("assignments/hello")
