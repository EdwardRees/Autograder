# Autograder

This is an autograder for Python. It assumes students are using GitHub Classrooms for their assignments.

The project clones student assignments, deletes the `.git` directory, inserts test code into each students' repository, and runs the test cases.

## Setup

### Installing Dependencies

- Run `pip3 install toml` to install toml

### Clone the project

Clone the project at `git@github.com:EdwardRees/Autograder.git`

### Setup Configuration

In the `config.toml` in the `config` folder, set the followign variables:

1. `course_name` should be set to the name of the GitHub classroom name or the GitHub organization.
2. `student_names` should be set to the `csv` file containing the student names and username pairs.
3. `debug mode` should be set to `true` if the output should include `debug` level logged values. Otherwise this can be `false` if only `info` level values are required.
4. `log_destination` should be set to the name of the log file.

### Adding the alias

Run `ln -s "$(pwd)/grade" /usr/local/bin/grade` to have access to using the `grade` command without needing to run it as `./grade`.

## Technology

- Python3
- toml
- logging

## Features

## CLA 

- `clean`: Clean the files corresponding to the given assignment
- `clone`: Clone the repositories locally
- `test`: Test the repositories against the cloned repositories and the test cases.
- `analyze`: Analyze the tested repositories.
- `--assignment <project/lab/inclass> --name <number/assignment name>`
- `--student <name>`: Name for the student to work with. This is optional, by default it will work with all students in the class.
- `--username <username>`: Same as the name for the student to work with. This will apply the choice against a username of a student. By default, it will use all students in the class instead of a specific student.

## How to use

`grade <clone/test/clean/analyze> --assignment <project/lab/inclass> --name <number/assignment name> --student <name> --username <student username>`

