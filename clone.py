from os import system, mkdir, remove, getcwd, chdir
from os.path import isdir

def generate_assignment_link(course_name, assignment_type, assignment_name, username):
    return f"git@github.com:{course_name}/{assignment_type}-{assignment_name}-{username}"

def nav_to_assignments():
    pwd = getcwd().split("/")
    if "autograder" == pwd[-1]:
        chdir("assignments")
        return getcwd().split("/")
    if pwd[-2:] != ['autograder', 'assignments']:
        assignment_idx = pwd.index("assignments")
        backtracks = len(pwd) - assignment_idx
        for _ in range(backtracks):
            chdir("..")
    return getcwd().split("/")


def clone_assignment(course_name, assignment_type, assignment_name, username):
    if assignment_type not in ['project', 'lab', 'inclass']:
        print(f"Invalid assignment type")
        return
    dir_name = f"{assignment_type}-{assignment_name}-{username}"
    if isdir(dir_name):
        system(f"rm {dir_name}")
    url = generate_assignment_link(course_name, assignment_type, assignment_name, username)

    system(f"git clone {url}")
    chdir(dir_name)
    system("rm -rf .git")
    chdir("..")

def clone(course_name, assignment_type, assignment_name, student_usernames):
    if assignment_type not in ["project", "lab", "inclass"]:
        print("Invalid assignment type")
        return
    chdir("assignments")
    if not isdir(f"{assignment_type}-{assignment_name}"):
        mkdir(f"{assignment_type}-{assignment_name}")
    chdir(f"{assignment_type}-{assignment_name}")
    for username in student_usernames:
        try:
            clone_assignment(course_name, assignment_type, assignment_name, username)
        except FileNotFoundError:
            continue
    chdir("..")

