import mosspy
from os import chdir, getcwd, path
from os.path import isdir
from util import navigate_to_dir, walklevel
import logging
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from bs4 import BeautifulSoup

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
    navigate_to_dir("assignments")
    chdir(f"{assignment_type}s/{assignment_type}-{assignment_name}")
    contents = ""
    with open("report.html", 'r') as f:
        contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    comparisons = soup.find_all("a")
    comparisons = [tag for tag in comparisons if len(tag.get_text().split(" ")) == 2 and "%" in tag.get_text().split(" ")[1]]
    pairs = {}
    for i, links in enumerate(comparisons):
        text = links.get_text()
        file_name, percentage = text.split(" ")

        # print(len(text))
        # print(i, file_name, percentage)
        username = (file_name.split("/")[-2]).split("-")[-1]
        percentage = int(percentage[1:percentage.index("%")])
        if percentage < 70:
            continue
        if i % 2 == 0:
            if username not in pairs:
                pairs[username] = []
            next = comparisons[i + 1]
            next_file_name, next_percentage = next.get_text().split(" ")
            next_username = (next_file_name.split("/")[-2]).split("-")[-1]
            if next_username not in pairs:
                pairs[next_username] = []
            next_percentage = int(next_percentage[1:next_percentage.index("%")])
            pairs[username].append({next_username: percentage})
            pairs[next_username].append({username: next_percentage})
        else:
            continue
    flags = {}
    for pair, paired in pairs.items():
        if pair not in flags:
            flags[pair] = []
        for group in paired:
            for name, score in group.items():
                flags[pair].append(name)
    print("Check the following users: ")
    for pair in pairs:
        for group in pairs[pair]:
            for name, score in group.items():
                print(f"\t- {pair} with {name}. Similarity score: {score}")
    return (pairs, flags)


def view_report(assignment_type, assignment_name):
    navigate_to_dir("assignments")
    chdir(f"{assignment_type}s/{assignment_type}-{assignment_name}")
    class RequestHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = 'report.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    handler_object = RequestHandler 

    PORT = 8000
    my_server = TCPServer(("", PORT), handler_object)
    try:
        logger.info(f"Serving on port: http://localhost:{PORT}")
        my_server.serve_forever()
    except KeyboardInterrupt:
        print()
        logger.info(f"Shutdown server on port {PORT}")
        my_server.shutdown()

    chdir("../..")
