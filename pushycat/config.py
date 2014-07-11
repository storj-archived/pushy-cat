import json

CONFIG_PATH = "/etc/pushycat/config.json"

class Config(object):
    def __init__(self, path=CONFIG_PATH):
        self.config_path = path
        with open(path) as f:
            self.conf = json.loads(f.read())

        with open(self.conf["hooks"]) as f:
            self._hooks = json.loads(f.read())

    def user(self):
        return self.conf["user"]

    def listen(self):
        return self.conf["listen"]

    def path(self):
        return self.conf["path"]

    def hooks(self):
        return self._hooks

    def scripts(self):
        return self.conf["scripts"]

    def add(self, url, branch, directory, user):
        """Register webhook whose command is just a git update"""

        # Removes any hook for the same repository/user/branch.
        self._hooks = [
                hook
                for hook in self._hooks
                if not matches(hook, url, branch, user)]

        self._hooks.append({
            "user":       user,
            "repository": url,
            "branch":     branch,
            "run":        ["{0}/create-or-update-git.sh".format(self.scripts()), directory]
            })

        self.serialize()


    def serialize(self):
        with open(self.conf["hooks"], "w") as f:
            f.write(json.dumps(self._hooks, indent=2))

def matches(hook, url, branch, user):
    return hook["user"] == user and hook["repository"] == url and hook["branch"] == branch
