import flask
import string

import sys
import logging

class HttpListener(object):
    def __init__(self, listen, path):
        self.host, self.port = string.split(listen, ":")
        self.port = int(self.port)

        self.app = flask.Flask("pushycat")
        self.events = {}

        self.app.add_url_rule(path, 'webhook', self.hook, methods=["POST"])


    def set_logging(self):
        file_handler = logging.StreamHandler(sys.stdout)
        file_handler.setLevel(logging.WARNING)
        self.app.logger.addHandler(file_handler)


    def add(self, repository, branch, fn):
        self.events[repository + "/" + branch] = fn


    def hook(self):
        event = flask.request.headers['X-GitHub-Event']

        if event == 'ping':
            return flask.jsonify(zen_level='maximal')

        if event == 'push':
            payload = flask.request.json
            repository = payload["repository"]["url"]
            branch     = payload["ref"].split("/")[-1]
            sha        = payload["after"]

            self.events[repository + "/" + branch](sha)

            return flask.jsonify(status="ok")

    def run(self):
        print "running http server"
        self.set_logging()
        self.app.run(host=self.host, port=self.port)
