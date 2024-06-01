# Autograder

This is an autograder for Python. It assumes students are using GitHub Classrooms for their assignments.

The project clones student assignments, deletes the `.git` directory, inserts test code into each students' repository, and runs the test cases. Additionally, this code also connects to moss, implementing a simple plagiarismchecker/code comparison to allow for a simple first-glance toward identifying potential cases of plagiarism.

## Setup

### Moss Setup

Go to [https://theory.stanford.edu/~aiken/moss/](https://theory.stanford.edu/~aiken/moss/) and follow the directions of getting an account/user id. Update the user id in the config once you have received the email.

### Installing Dependencies

- Run `pip3 install -r requirements.txt`

### Clone the project

Clone the project at `git@github.com:EdwardRees/Autograder.git`

### Setup Configuration

Rename the `sample_config.toml` into `config.toml`.

In the `config.toml` in the `config` folder, set the following variables:

1. `course_name` should be set to the name of the GitHub classroom name or the GitHub organization.
2. `student_names` should be set to the `csv` file containing the student names and username pairs.
3. `test_repo` should be set the GitHub repository that contains testcases.
4. `moss_userid` should be the user id given by moss after creating an account here [https://theory.stanford.edu/~aiken/moss/](https://theory.stanford.edu/~aiken/moss/)
5. `compare_with_test` should be `true` or `false` if the plagiarism comparisons should be run when the code is tested too.
6. `debug mode` should be set to `true` if the output should include `debug` level logged values. Otherwise this can be `false` if only `info` level values are required.
7. `log_destination` should be set to the name of the log file.
8. `error_log_destination` should be set to the name of the error log file.

### Adding the alias

Run `ln -s "$(pwd)/grade" /usr/local/bin/grade` to have access to using the `grade` command without needing to run it as `./grade`.

## Technology

- Python3
- toml
- mosspy
- logging
- shutil

## Features

## CLA

- `clean`: Clean the files corresponding to the given assignment
- `clone`: Clone the repositories locally
- `test` or `grade`: Test the repositories against the cloned repositories and the test cases.
- `analyze`: Analyze the tested repositories.
- `compare`: Compare the repositories for a given assignment based on moss.
- `--assignment <project/lab/inclass/tests> --name <number/assignment name>`
- `--student <name>`: Name for the student to work with. This is optional, by default it will work with all students in the class.
- `--username <username>`: Same as the name for the student to work with. This will apply the choice against a username of a student. By default, it will use all students in the class instead of a specific student.
- `--pull` or `--update`: Don't clone, but pull the given project. If `--pull` is called on `test`, pull the tests.
- `--parse`: Works with compare type: Parse the comparison results and display flagged submissions.
- `--view`: Works with compare type: View the comparison results in a web instance for the flagged submissions.

## How to use

`grade <clone/test/clean/analyze/compare> --assignment <project/lab/inclass/tests> --name <number/assignment name> --student <name> --username <student username> --pull --parse --view`

### Use Examples

- `grade clone --assignment lab --name 5 --username johndoe`: Clone Lab 5 for johndoe specifically
- `grade clone --assignment lab --name 5`: Clone all Lab 5s
- `grade clone --assignment tests`: Clone the tests

- `grade test --pull`: Pull the test cases
- `grade test --assignment lab --name 5`: Test all the lab 5s, writes output into `assignmebts/lab/lab-5/results.txt`
- `grade test --assignment lab --name 5 --username johndoe`: Test Lab 5 for johndoe specifically

- `grade clean --assignment tests`: Remove the tests
- `grade clean --assignment lab --name 5`: Remove the lab 5 repositories
- `grade clean --assignment lab --name 5 --username johndoe`: Clean Lab 5 for johndoe specifically

- `grade compare --assignment lab --name 5`: Run the comparison for plagiarism scripts for Lab 5
- `grade compare --assignment lab --name 5 --parse`: Do not run the comparison, only parse the output
- `grade compare --assignment lab --name 5 --view`: Do not run the comparison, view the output in a web view

## Todos

- [ ] Fix logging to files
- [ ] Implement Analyze feature (analyze.py)
- [x] Implement clean on individual student
- [ ] Fix testing individual student resets the `assignments/{assignment_type}s/results.txt`
- [ ] Implement clone for inclass
    - [ ] Technically a fix instead, but the format for inclass differs from the labs and project naming convention.
- [x] Implement clone for starter code too: `assignments/{assignment_type}-{assignment_name}-starter`
- [ ] Implement moss for automated plagiarism detection (compare.py)
    - [ ] Create one repository for GenAI. Store the output from code generated by GenAI
    - [ ] Include expected code for some of the projects. This can simply be under an "expected" repository.
    - [x] Config option to include comparison initially when running tests. Comparison score will simply add a "Flagged for Plagiarism" to the `results.txt` file.
