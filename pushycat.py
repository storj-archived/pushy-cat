#!/usr/bin/env python

import config
import http
import client
import os
import pwd
import sys

CONFIG_PATH = "/etc/pushycat/config.json"
CONFIG_PATH = "config.json.example"

def setup(conf):
    clients = {}
    listener = http.HttpListener(conf.listen(), conf.path())

    for hook in conf.hooks():
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
                lambda sha: c.notify(repository, branch, sha))

    return (listener, clients.values())


def chuser(username):
    uid = pwd.getpwnam(username).pw_uid

    if uid != 0:
        os.setgid(uid)
        os.setuid(uid)


def load_json_file(filename):
    with open(filename) as f:
        return json.loads(f.read())

def run(filename):
    conf = config.Config(filename)

    listener, clients = setup(conf)

    if os.fork() == 0:
        chuser(conf.user())
        listener.run()
        sys.exit(-1)

    for client in clients:
        if os.fork() == 0:
            chuser(client.user)
            client.run()
            sys.exit(-1)

    for i in xrange(0, 1 + len(clients)):
        os.wait()

run(CONFIG_PATH)
