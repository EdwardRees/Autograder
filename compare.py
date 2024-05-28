import mosspy

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
        self.moss.send(lambda file_path, display_name: print("*", end="", flush=True))
        print()

        print(f"Report URL: {url}")

        self.moss.saveWebPage(url, f"assignments/{self.assignment_type}s/{self.assignment_type}-{self.assignment_name}/report.html")

        mosspy.download_report(url, "submission/report/", connections=8, log_level=10, on_read=lambda url: print('*', end='', flush=True)) 


def compare_files(config, assignment_type, assignment_name, starter_code):
    user_id = config.get("class").get("moss_user_id")
    c = Compare()

