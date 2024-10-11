# slack-image-dump
> Dump slack images containing text keywords

Leverages Slack search's built-in image-to-text/OCR capabilities to find images containing the specified text. 
Use it to find screenshots of valid secrets or other interesting images. 

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

__Example usage:__
```
slack-image-dump --query '"client_secret"' --workspace yourcompanyname --cookie xoxd-xxxxxxxxxxxxxxxxxxx
```
This downloads each image in the result set to a newly created directory called `slack-image-dump-client_secret/`.
