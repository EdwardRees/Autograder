# Autograder

This is an autograder for Python. It assumes students are using GitHub Classrooms for their assignments.

The project clones student assignments, deletes the `.git` directory, inserts test code into each students' repository, and runs the test cases.

## Setup

### Clone the project

Clone the project at `git@github.com:EdwardRees/Autograder.git`

### Setup Configuration

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

`./grade <clone/test/clean/analyze> --assignment <project/lab/inclass> --name <number/assignment name> --student <name> --username <student username>`

