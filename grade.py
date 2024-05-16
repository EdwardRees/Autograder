#!/usr/bin/env python3
from sys import argv
from clone import clone
from util import get_course_name, get_name_username_pair, get_username_name_pair, get_student_usernames, read_config, read_csv
from clean import clean


def parse_args(argv):
  arguments = {}
  argv = argv[1:]
  command_line_type = argv[0]
  arguments["type"] = command_line_type
  assignment_flag = argv.index("--assignment")
  arguments["assignment_type"] = argv[assignment_flag + 1]
  name_flag = argv.index("--name")
  arguments["assignment_name"] = argv[name_flag + 1]
  if "--student" in argv:
    student_flag = argv.index("--student")
    arguments["student_name"] = argv[student_flag + 1]
  if "--username" in argv:
    username_flag = argv.index("--username")
    arguments["username"] = argv[username_flag + 1]
  return arguments


def main():
  if len(argv) < 6:
    print(f"Invalid usage: {argv[0]} <clone/grade/test/analyze/clean> --assignment <project/lab/inclass> --name <number/assignment name> --student <student name> --username <username>")
    return
  config = read_config("config/config.toml")
  arguments = parse_args(argv)
  course_name = get_course_name(config)
  student_csv = read_csv(config.get("class").get("student_names"))
  usernames = get_student_usernames(student_csv)

  if arguments.get("type") == "clone":
    clone(course_name, arguments.get("assignment_type"), arguments.get("assignment_name"), usernames)
  elif arguments.get("type") == "clean":
    clean(arguments.get("assignment_type"), arguments.get("assignment_name"))


if __name__ == "__main__":
  main()
