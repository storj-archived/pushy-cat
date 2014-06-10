import subprocess
import os
import json

class Client(object):
    def __init__(self, user, pipe):
        self.user = user
        self.events = {}

        rfd, wfd = pipe

        self.reader = os.fdopen(rfd,"r")
        self.writer = os.fdopen(wfd,"w")

    def add(self, repository, branch, command):
        self.events[repository + "/" + branch] = command

    def execute(self, repository, branch, sha):
        command = self.events[repository + "/" + branch]

        subprocess.call(command + [repository, branch, sha])

    def notify(self, repository, branch, sha):
        print("notifying with uid =", os.getuid())

        self.writer.write(json.dumps({
            "repository": repository,
            "branch": branch,
            "sha": sha
        }) + "\n")
        self.writer.flush()

    def run(self):
        print("running client uid({0})".format(os.getuid()))

        while True:
            payload = json.loads(self.reader.readline())

            print("notified with uid({0}): {1}".format(os.getuid(), payload))
            self.execute(
                    payload["repository"],
                    payload["branch"],
                    payload["sha"])
