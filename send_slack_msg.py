import json, requests, sys


def format_slack_data(score, title, message):
    if score == "5":
        stars = ":star::star::star::star::star:"
    elif score == "4":
        stars = ":star::star::star::star:"
    elif score == "3":
        stars = ":star::star::star:"
    elif score == "2":
        stars = ":star::star:"
    elif score == "1":
        stars = ":star:"
    else:
        stars = ""
    slack_data = {
        "username": "AppReview",
        "icon_emoji": ":android:",
        #"channel" : "#somerandomcahnnel",
        "text": title,
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": stars,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    slack_data_formated = json.dumps(slack_data)
    return slack_data_formated, byte_length

def send_msg(webhook_url, message, byte_length):
    headers = {
                'Content-Type': "application/json",
                'Content-Length': byte_length
            }
    response = requests.request("POST", webhook_url, headers=headers, data=message)
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text))
