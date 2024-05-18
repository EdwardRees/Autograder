from sys import argv
from clone import clone, get_username, clone_tests, test_cloned_check
from util import get_course_name, get_name_username_pair, get_username_name_pair, get_student_usernames, read_config, read_csv
from clean import clean
import logging

logger = logging.getLogger(__name__)

def parse_args(argv):
  arguments = {}
  argv = argv[1:]
  command_line_type = argv[0]
  arguments["type"] = command_line_type
  assignment_flag = argv.index("--assignment")
  arguments["assignment_type"] = argv[assignment_flag + 1]
  if "--name" in argv:
    name_flag = argv.index("--name")
    arguments["assignment_name"] = argv[name_flag + 1]
  if "--student" in argv:
    student_flag = argv.index("--student")
    arguments["student_name"] = argv[student_flag + 1]
  if "--username" in argv:
    username_flag = argv.index("--username")
    arguments["username"] = argv[username_flag + 1]
  if "--pull" in argv or "--update" in argv:
    arguments["pull"] = True
  return arguments

def logger_setup(config):
  stream_handle = logging.StreamHandler()
  file_handle = logging.FileHandler(f"log/{config.get("log").get("log_destination")}")

  stream_handle.setLevel(logging.DEBUG if config.get("log").get("debug") else logging.INFO)
  file_handle.setLevel(logging.WARNING)

  stream_handle_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
  file_handle_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

  stream_handle.setFormatter(stream_handle_format)
  file_handle.setFormatter(file_handle_format)

  logger.addHandler(stream_handle)
  logger.addHandler(file_handle)

  return logger


def main():
  if len(argv) < 3:
    print(f"Invalid usage: {argv[0]} <clone/grade/test/analyze/clean> --assignment <project/lab/inclass/tests> --name <number/assignment name> --student <student name> --username <username> --pull")
    return
  config = read_config("config/config.toml")
  
  logger_setup(config)

  test_repos = config.get("class").get("test_repo")
  arguments = parse_args(argv)
  course_name = get_course_name(config)
  student_csv = read_csv(config.get("class").get("student_names"))
  usernames = get_student_usernames(student_csv)
  name_username_dictionary = get_name_username_pair(student_csv)

  if arguments.get("type") == "clone":
    username = ""
    if "student_name" in arguments:
      username = get_username(name_username_dictionary, arguments.get("student_name"))
      if username is None:
        logger.error(f"Cannot clone assignment for non-existent student")
        return
      usernames = [username]
    elif "username" in arguments:
      if arguments.get("username") not in usernames:
        logger.error(f"Cannot clone assignment for non-existent student")
        return
      username = arguments.get("username")
      usernames = [username]
    if arguments.get('assignment_type') == "tests":
      clone_tests(config.get("class").get("test_repo"))
    clone(course_name, arguments.get("assignment_type"), arguments.get("assignment_name"), usernames)
  elif arguments.get("type") == "clean":
    clean(arguments.get("assignment_type"), arguments.get("assignment_name"))
  elif arguments.get("type") == "test":
    if "pull" in arguments:
      # Simply pull the tests, don't clone the tests again. Just call pull_tests()
      pass
    username = ""
    if "student_name" in arguments:
      username = get_username(name_username_dictionary, arguments.get("student_name"))
      if username is None:
        logger.error(f"Cannot clone assignment for non-existent student")
        return
      usernames = [username]
    elif "username" in arguments:
      if arguments.get("username") not in usernames:
        logger.error(f"Cannot clone assignment for non-existent student")
        return
      username = arguments.get("username")
      usernames = [username]
    if not test_cloned_check(arguments.get("assignment_type"), arguments.get("assignment_name")):
      logger.info("Tests must be cloned first!")
      clone_tests(config.get("class").get("test_repo"))


if __name__ == "__main__":
  main()
