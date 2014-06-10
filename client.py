import subprocess
import string
import os

class Client(object):
    def __init__(self, user, pipe):
        self.user = user
        self.events = {}

        rfd, wfd = pipe

        self.reader = os.fdopen(rfd,"r")
        self.writer = os.fdopen(wfd,"w")

    def add(self, repository, branch, command):
        self.events[repository + "/" + branch] = command

    def notify(self, repository, branch):
        subprocess.call(
                self.events[repository + "/" + branch],
                shell=True)

    def run(self):
        print "running client with uid =", os.getuid()
        while True:
            line = self.reader.readline()
            self.notify(*string.rsplit(line,'/', 1))
