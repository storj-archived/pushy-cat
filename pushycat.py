#!/usr/bin/env python

import flask
import registry

app = flask.Flask(__name__)

def get_registry():
    r = getattr(flask.g, '_registry', None)
    if r is None:
        r = flask.g._registry = registry.Registry("hooks.json")

    return r


@app.route("/hook/<repo>", methods=['POST'])
def hook(repo):
    if flask.request.headers['X-GitHub-Event'] == 'ping':
        return flask.jsonify(zen_level="super")

    if flask.request.headers['X-GitHub-Event'] == 'push':
        branch = flask.request.json["ref"].split("/")[-1]
        sha    = flask.request.json["after"]

        get_registry().notify(repo, branch, sha)

        return flask.jsonify(status="ok")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
