import config
import argparse

CONFIG_PATH = "/etc/pushycat/config.json"
CONFIG_PATH = "config.json.example"

def main():
    parser = argparse.ArgumentParser(
            description='Adds a hook to pushycat that automatically updates your repository.')

    parser.add_argument('url')
    parser.add_argument('directory')
    parser.add_argument('user')
    parser.add_argument('--branch', default='master')

    options = parser.parse_args()

    conf = config.Config(CONFIG_PATH)

    conf.add(options.url, options.branch, options.directory, options.user)

    print "webhook succesfully added."
    print "Please restart pushycat (service pushycat restart)"

if __name__ == "__main__":
    main()
