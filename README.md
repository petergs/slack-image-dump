# slack-image-dump
> Dump slack images containing text keywords

# usage
```
usage: slack-image-dump [-h] -q QUERY -w WORKSPACE [-c COOKIE] [-u USER_AGENT]

Commandline tool to dump slack images from a workspace based on a specified query

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Slack keyword search query
  -w WORKSPACE, --workspace WORKSPACE
                        Slack workspace url to search
  -c COOKIE, --cookie COOKIE
                        Slack d cookie extracted from a browser session (starting with `xoxd-`)
  -u USER_AGENT, --user-agent USER_AGENT
                        Optional User-Agent override

slack-image-dump expects a cookie supplied with the -c parameter or set with the environment variable SLACK_COOKIE
```
