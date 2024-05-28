import mosspy
from os import chdir, getcwd, path
from os.path import isdir
from util import navigate_to_dir, walklevel
import logging

logger = logging.getLogger(__name__)
curr_dir = path.dirname(path.realpath(__file__))


class Compare:
    def __init__(self, userid, assignment_type, assignment_name):
        self.userid = userid
        self.moss = mosspy.Moss(self.userid, "python")
        self.assignment_name = assignment_name
        self.assignment_type = assignment_type

    def add_files(self, base_files, files):
        for base_file in base_files:
            self.moss.addBaseFile(base_file)
        for file in files:
            self.moss.addFile(file)

    def send(self):
        url = self.moss.send(
            lambda file_path, display_name: print("*", end="", flush=True)
        )
        print()

        print(f"Report URL: {url}")

        # with open(f"report.html", "w") as f:
        #     print(f"Created report.html")
        #
        self.moss.saveWebPage(url, f"report.html")

        mosspy.download_report(
            url,
            "submission/report/",
            connections=8,
            log_level=10,
            on_read=lambda url: print("*", end="", flush=True),
        )


def compare_files(config, assignment_type, assignment_name):
    user_id = config.get("class").get("moss_user_id")
    c = Compare(user_id, assignment_type, assignment_name)
    base_files = []
    student_files = []
    navigate_to_dir("assignments")
    chdir(f"{assignment_type}s/{assignment_type}-{assignment_name}")
    logger.info(getcwd())
    for root, dirs, files in walklevel(
        f"{assignment_type}-{assignment_name}-starter-code"
    ):
        for file in files:
            if file.endswith(".py"):
                base_files.append(f"{getcwd()}/{root}/{file}")
    for root, dirs, files in walklevel("."):
        for dir in dirs:
            if dir.endswith("starter-code"):
                continue
            for inner_root, inner_dirs, inner_files in walklevel(dir):
                for file in inner_files:
                    if file == "test.py":
                        continue
                    if file.endswith(".py"):
                        student_files.append(f"{getcwd()}/{inner_root}/{file}")
    c.add_files(base_files, student_files)
    c.send()
    chdir("../..")


def parse_report(assignment_type, assignment_name):
    """
    Parse the report created and find most problematic student code bases
    """
    pass


def view_report(assignment_type, assignment_name):
    """
    View the report by spinning up a simple python server to serve the report.html
    """
    pass
