pushycat
=========

Listens to GitHub webhooks and executes scripts accordingly.

Use case: automatically update static websites.

## Installation

If you're running Ubuntu, the preferred method of installation is through a deb
package.

If you cannot or do not want to install pushycat through a deb package, clone
this repository, install the required eggs (`pip install -r requirements.txt`),
set up the configuration files, and run the daemon:

```
pushycatd --conf /path/to/config.json
```

If you wish to run hook scripts with multiple users, pushycatd must be run as
root, so that it can create child processes with different users.


### Configuration

The main configuration file lives, by default, in `/etc/pushycat/config.json`.
You can see an example in `examples/debian/config.json`. It supports the following settings:

- user - username that should run the http server
- listen - listen address, in "host:port" format, for the http server
- path - http path where the webhooks are to be sent
- hooks - file path for the hook definition file
- scripts - file path for the default scripts directory

The user setting can only be different from the user running `pushycatd` if it
is running as root. The last setting is only required if you wish to use the
`pushycat-add` helper. It requires that a file called `create-or-update-git.sh`
exists in that directory.


#### Hooks configuration

Create a hooks.json similar to the provided hooks.example.json. For example, if
you want to track the main branch on a repository, so that it automatically
pulls a local copy, you would set it up like so:

```json
[
  {
    "user":       "storj",
    "repository": "https://github.com/Storj/storj.io",
    "branch":     "main",
    "run":        ["/path/to/create-or-update-git.sh", "/var/www/storj.io"]
  }
]
```

Three extra arguments will be appended to the executable whenever it is called:
repository url, branch name, and the most recent commit hash. In the example
above, `create-or-update-git.sh` would be called with four arguments:

```
create-or-update-git.sh
    "/var/www/storj.io"
    "https://github.Storj/storj.io"
    "main"
    "b8e38b7b05e5fe3130ee788c211020bc5af2415b"
```

Due to this behaviour, it is recommended that you always create a wrapper
script to avoid passing unwanted arguments to your executable.

If you just wish to update a git directory whenever there's a push event, you can use
the `pushycat-add` tool, instead of editing the hooks file by hand. The following command
will add the json shown above:

```
pushycat-add https://github.com/Storj/storj.io /var/www/storj.io storj
```

This tool also supports two optional arguments: `--conf /path/to/conf` and
`--branch branch-name`.


#### GitHub webhook configuration

Add an url in the form `http://host:portpath` to your GitHub project, according to
the settings in `/etc/pushycat/config.json`.

For example, if you set the listen setting to `0.0.0.0:8080` and path to `/webhook/`,
the url should be something like `http://your-ip:8080/webhook/`.
