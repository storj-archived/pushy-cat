pushy-cat
=========

Listens to Github webhooks and executes scripts accordingly.

Use case: automatically update static websites.

pushycat allows you to configure a webhook listener that does one of the following:
- run a script
- write the pushed commit hash to a file


## Installation

```bash
git clone https://github.com/Storj/pushy-cat.git /your/local/path
cd /your/local/path
go build *.go
```


## Configuration

Create a hooks.json similar to the provided `examples/hooks.json`.

Here's a detailed example that contains both the executable and the file commands:

```json
{
  "listen": "0.0.0.0:8080",
  "hooks":[
    {
      "repository": "repository-name",
      "branch":     "master",
      "execute":    "/path/to/script.sh"
    },
    {
      "repository": "other-repository-name",
      "branch":     "development",
      "file":       "/path/to/other-repository-name.commit"
    }
  ]
}
```

This will listen to any github events being sent to
`your-domain.com/repository-name` and `your-domain.com/other-repository-name`

The executable string will be run as an argument to `bash -c`.


### Daemon setup

To have pushycat always running, you need to setup upstart, init, or supervisord.
The `examples` directory contains some sample configurations to get you started.
