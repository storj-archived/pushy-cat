import flask
import string

class HttpListener(object):
    def __init__(self, listen):
        self.host, self.port = string.split(listen, ":")
        self.port = int(self.port)

        self.app = flask.Flask("pushycat")
        self.events = {}

        self.app.add_url_rule(
                '/hook/<repo>',
                'hook',
                lambda repo: self.hook(repo))

    def add(self, repository, branch, fn):
        self.events[repository + "/" + branch] = fn


    def hook(self, repo):
        event = flask.request.headers['X-GitHub-Event']

        if event == 'ping':
            return flask.jsonify(zen_level='super')

        if event == 'push':
            payload = flask.request.json
            branch  = payload["ref"].split("/")[-1]
            sha     = payload["after"]

            self.events[repository + "/" + branch]()

            return flask.jsonify(status="ok")

    def run(self):
        self.app.run(debug=True, host=self.host, port=self.port)
