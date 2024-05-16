import toml
from csv import reader

def read_csv(filename):
    try:
        contents = []
        with open(filename, 'r') as f:
            for line in reader(f):
                    contents.append(line)
        return contents
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []

def read_toml(filename):
    try:
        with open(filename, 'r') as f:
            return toml.load(f)
    except (FileNotFoundError, TypeError, toml.TomlDecodeError) as e:
        print(f"Error: {e}")
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


if __name__ == "__main__":
    student_csv = read_csv("config/student_accounts.csv")
    print(get_username_name_pair(student_csv))
    print(get_name_username_pair(student_csv))
    print(get_student_usernames(student_csv))
    # print(read_toml("config.toml"))
