import logging
from toml import load, TomlDecodeError
from csv import reader
from os import path, walk, chdir, getcwd
from os.path import isdir, sep

logger = logging.getLogger(__name__)
curr_dir = path.dirname(path.realpath(__file__))


def walklevel(dir, level=0):
    dir = dir.rstrip(path.sep)
    logger.info(dir)
    assert isdir(dir)
    num_sep = dir.count(path.sep)
    for root, dirs, files in walk(dir):
        yield root, dirs, files
        inner_num_sep = root.count(path.sep)
        if num_sep + level <= inner_num_sep:
            del dirs[:]


def navigate_to_dir(dir):
    # Navigate to directory after /autograder
    pwd = getcwd().split("/")
    if "autograder" == pwd[-1]:
        if isdir(dir):
            chdir(dir)
        return getcwd().split("/")
    elif pwd[-2:] != ["autograder", dir]:
        dir_idx = pwd.index(dir)
        backtracks = len(pwd) - dir_idx
        for _ in range(backtracks):
            chdir("..")
    logger.debug(f"Navigated to {getcwd()}")
    return getcwd().split("/")


def read_csv(filename):
    try:
        contents = []
        with open(filename, "r") as f:
            for line in reader(f):
                contents.append(line)
        logger.info(f"Successfully read {filename}")
        return contents
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        return []


def read_toml(filename):
    try:
        with open(filename, "r") as f:
            logger.info(f"Successfully read {filename}")
            return load(f)
    except (FileNotFoundError, TypeError, TomlDecodeError) as e:
        logger.error(f"Error: {e}")
        return {}


def read_config(filename):
    return read_toml(filename)


def get_course_name(config):
    return config.get("class").get("course_name")


def get_name_username_pair(student_csv):
    accounts = {}
    contents = student_csv[1:]
    for name, username, notes in contents:
        accounts[name] = username
    return accounts


def get_username_name_pair(student_csv):
    accounts = {}
    contents = student_csv[1:]
    for name, username, notes in contents:
        accounts[username] = name
    return accounts


def get_student_usernames(student_csv):
    usernames = []
    contents = student_csv[1:]
    for _, username, _ in contents:
        usernames.append(username)
    return usernames
