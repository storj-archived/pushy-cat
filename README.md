pushy-cat
=========

Listens to Github webhooks and executes scripts accordingly.

Use case: automatically update static websites.

#### Installation

Create a hooks.json similar to the provided hooks.example.json. For example, if
you want to track the master branch on a repository, so that it automatically
pulls a local copy, you would set it up like so:

```json
{
  "hooks":[
    {
      "repository": "repository-name",
      "branch":     "master",
      "deploy":     "/path/to/script.sh"
    }
  ]
}
```

/path/to/script.sh would contain `cd /path/to/local/repo; git pull` (be sure to
mark it as executable, with chmod +x /path/to/local/repo).

Then, set up a gunicorn webserver pointing to pushycat:app and add a git
webhook pointing to your-domain.com/repository-name.

##### Example setup commands

```bash
git clone https://github.com/Storj/pushy-cat.git
cd pushy-cat
virtualenv .env --prompt [pushycat]
source .env/bin/activate
pip install -r requirements.txt
```

You still need to configure hooks.json and any scripts to execute.

#### Gunicorn+supervisord setup

If you have supervisord installed, you can use it to automatically run
pushycat as a gunicorn daemon, using the following config file:

```ini
[program:pushycat]
command=/home/pushycat/pushy-cat/.env/bin/gunicorn -w 2 -b 127.0.0.1:5100 pushycat:app
directory=/home/pushycat/pushy-cat
user=pushycat

autostart=true
autorestart=true
redirect_stderr=true
```
