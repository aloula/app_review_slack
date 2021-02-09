#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Simple script to extract Google Play app comments and sent it to Slack
# Author: Alexsander Loula - 2021/2/9

import sys, os
from datetime import datetime
from google_play_scraper import Sort, reviews
from send_slack_msg import send_msg, format_slack_data

webhook_url = 'put_your_slack_webhook_url_here' # https://api.slack.com/messaging/webhooks#create_a_webhook
app_name = 'put_your_app_name_here' #example: com.nianticlabs.pokemongo


# functions
def read_last_update():
    with open('last_update.txt', 'r') as f:
        last_line = f.readlines()[-1]
        return last_line


def write_last_update(data):
     with open("last_update.txt", 'a') as f:
         last_upate = f.write(data + '\n')
         return last_upate


def get_results():
    result, continuation_token = reviews(
        app_name,
        lang='pt', # defaults to 'en'
        country='br', # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
        count=10, # defaults to 100
        filter_score_with=None # defaults to None(means all score)
    )
    result, _ = reviews(
        app_name,
        continuation_token=continuation_token # defaults to None(load from the beginning)
    )
    return result


def extract_results(results, last_update): 
    for i in results:
        user_name = str(i["userName"])
        content = str(i["content"])
        score = str(i["score"])
        app_version = str(i["reviewCreatedVersion"])
        datetime = str(i["at"])
        # Only send since the last update
        if last_update < datetime:
            title = ("Usuário: " + user_name + " | App: " + app_version + " | " + datetime)
            message = ("Comentário: " + content)
            slack_data, byte_length = format_slack_data(score, title, message)
            send_msg(webhook_url, slack_data, byte_length)


if __name__ == "__main__":
    now = str(datetime.today())[0:19]
    print("Starting extraction", now)
    last_update = read_last_update()
    print("Sending comments since", last_update)
    results = get_results()
    extract_results(results, last_update)
    write_last_update(now)
    print("Done!")
    sys.exit(0)    