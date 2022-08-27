# SlackBot For YBKZ members

This slackbot source code is to keep YBKY members updated about their daily progress on [this problem solving platform](https://binarysearch.com)

## How to set up

- Clone this repository
- Create .env file
  - add SLACK_TOKEN and CHANNEL_NAME
- Run main.py to send an update to CHANNEL_NAME

## Running on a server

You can set up a cron job to run this bot at given intervals

- Paste the values for your environment for crontab.md
- Open crontab
  - `crontab -e`
- Paste the content of crontab.md once you update it
