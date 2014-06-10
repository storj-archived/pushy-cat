#!/usr/bin/env python

import http
import client
import json
import os
import pwd

def client_notify(client, repo, branch):
    def f():
        client.writer.write("{0}/{1}\n".format(repo, branch))

    return f


def setup(config):
    hooks = load_json_file(config["hooks"])

    clients = {}
    listener = http.HttpListener(config["listen"])

    for hook in hooks:
        user       = hook["user"]
        repository = hook["repository"]
        branch     = hook["branch"]
        run        = hook["run"]

        c = clients.get(user, None)
        if c is None:
            c = clients[user] = client.Client(user, os.pipe())

        c.add(repository, branch, run)
        listener.add(
                repository,
                branch,
                client_notify(c, repository, branch))

    return (listener, clients.values())


def chuser(username):
    uid = pwd.getpwnam(username).pw_uid

    os.setuid(uid)
    os.setgid(uid)


def load_json_file(filename):
    with open(filename) as f:
        return json.loads(f.read())

def run(filename):
    config = load_json_file(filename)

    listener, clients = setup(config)

    if os.fork() == 0:
        chuser(config["user"])
        listener.run()
        os.exit(-1)

    for client in clients:
        if os.fork() == 0:
            chuser(client.user)
            client.run()
            os.exit(-1)

    for i in xrange(0, 1 + len(clients)):
        os.wait()

run("/etc/pushycat/config.json")
