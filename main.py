from sys import argv, stdout
from clone import clone, get_username, clone_tests, test_cloned_check, pull_tests
from util import get_course_name, get_name_username_pair, get_username_name_pair, get_student_usernames, read_config, read_csv
from clean import clean, clean_tests, clean_single
import logging
from test import add_test_to_repo, run_tests
from compare import compare_files, parse_report, view_report

logger = logging.getLogger(__name__)

def help_menu():
  print(f"""
        {argv[0]} <clone/test/grade/clean/analyze> --assignment <project/lab/inclass/tests> --name <assignment name or number> --username <username of student> --student <name of student> --pull
        Options:
        - Clone: Clone the given assignment repository
        - Test/Grade: Run the tests on the given assignment 
        - Clean: Remove the files associated with the assignment or tests
        - Analyze: Run simple analysis on the assignment results from the tests performed
        - Compare: Compare student submissions with each other using Moss.
        Command Line Flags:
        - --assignment: The type of assignment to perform the optional action on: project, lab, inclass, or on the tests themselves
        - --name: The name of the assignment, used to concatenate on top of the project, lab, or inclass. For example, this flag would take a number for the labs and projects, but take the name of the inclass for the inclass.
        - --username: An optional flag used to perform the optional action on a specific student.
        - --student: An optional flag used to perform the optional action on a specific student, with the student's name provided.
        - --pull: An optional flag used to pull the latest test cases.
        - --parse: An optional flag used to parse the report from the code comparisons
        - --view: An optional flag used to view the report from the code comparisons
  """)

def not_in(argv, flags):
  for flag in flags:
    if flag in argv:
      return False
  return True

def parse_args(argv):
  arguments = {}
  argv = argv[1:]
  command_line_type = argv[0]
  arguments["type"] = command_line_type
  if not_in(argv, ["--assignment", "--pull", "-h"]):
    logger.error("Missing assignment flag!")
    exit(-2)
  if "--assignment" in argv:
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
  if "--parse" in argv:
    arguments["parse"] = True
  if "--view" in argv:
    arguments["view"] = True
  if "--help" in argv or "-h" in argv:
    arguments["help"] = True
  return arguments

def main():
  if len(argv) < 3:
    print(f"Invalid usage: {argv[0]} <clone/grade/test/analyze/clean> --assignment <project/lab/inclass/tests> --name <number/assignment name> --student <student name> --username <username> --pull --parse --view")
    return
  config = read_config("config/config.toml")

  logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG if config.get("log").get("debug") else logging.INFO)

  stream_handle = logging.StreamHandler(stream=stdout)
  file_handle = logging.FileHandler(f"log/{config.get("log").get("log_destination")}")
  error_handle = logging.FileHandler(f"log/{config.get("log").get("error_log_destination")}")

  stream_handle.setLevel(logging.DEBUG if config.get("log").get("debug") else logging.INFO)
  file_handle.setLevel(logging.DEBUG)
  error_handle.setLevel(logging.WARNING)

  stream_format = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s")
  file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

  stream_handle.setFormatter(stream_format)
  file_handle.setFormatter(file_format)
  error_handle.setFormatter(file_format)

  logger.addHandler(stream_handle)
  logger.addHandler(file_handle)
  logger.addHandler(error_handle)

  logger.setLevel(logging.DEBUG)

  # print(logger, logger.handlers)

  test_repos = config.get("class").get("test_repo")
  arguments = parse_args(argv)
  course_name = get_course_name(config)
  student_csv = read_csv(config.get("class").get("student_names"))
  usernames = get_student_usernames(student_csv)
  name_username_dictionary = get_name_username_pair(student_csv)

  if arguments.get("help"):
    help_menu()
    return

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
    else:
      clone(course_name, arguments.get("assignment_type"), arguments.get("assignment_name"), usernames)

  elif arguments.get("type") == "clean":
    if arguments.get("assignment_type") == "tests":
      clean_tests()
    else:
      if "username" in arguments:
        username = arguments.get("username")
        if username not in usernames:
          logger.error(f"Cannot clean assignment for non-existent student")
          return
        clean_single(arguments.get("assignment_type"), arguments.get("assignment_name"), username)
      elif "student_name" in arguments:
        username = get_username(name_username_dictionary, arguments.get("student_name"))
        if username is None:
          logger.error(f"Cannot clean assignment for non-existent student")
          return
        clean_single(arguments.get("assignment_type"), arguments.get("assignment_name"), username)
      else:
        clean(arguments.get("assignment_type"), arguments.get("assignment_name"))

  elif arguments.get("type") == "compare":
    if arguments.get("parse"):
      print(parse_report(arguments.get("assignment_type"), arguments.get('assignment_name'))[2])
    elif arguments.get("view"):
      view_report(arguments.get("assignment_type"), arguments.get("assignment_name"))
    else:
      print(compare_files(config, arguments.get("assignment_type"), arguments.get("assignment_name")))

  elif arguments.get("type") == "test" or arguments.get("type") == "grade":
    if "pull" in arguments:
      pull_tests()
      return
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
    add_test_to_repo(arguments.get("assignment_type"), arguments.get("assignment_name"), usernames)
    plagiarism_checks = None
    if config.get("moss").get("compare_with_test"):
      plagiarism_checks = parse_report(arguments.get("assignment_type"), arguments.get("assignment_name"))[0]
    run_tests(arguments.get("assignment_type"), arguments.get("assignment_name"), usernames, plagiarism_checks)


  


if __name__ == "__main__":
  main()
