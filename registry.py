import json
import subprocess

class Registry:
    def __init__(self, filename):
        self.potato = json.loads(open(filename).read())["hooks"]

    def notify(self, repo, branch, sha):
        hook = self.hook_for(repo, branch)

        if hook is None:
            return

        if "deploy" in hook:
            subprocess.call(hook["deploy"], shell=True)

        if "file" in hook:
            with open(hook["file"], "w") as f:
                f.write(sha)


    def hook_for(self, repo, branch):
        candidates = [
            hook
            for hook in self.potato
            if hook["repository"] == repo and
               hook["branch"] == branch]

        if len(candidates) == 0:
            return None
        else:
            return candidates[0]
