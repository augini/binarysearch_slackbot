from time import clock_getres
from slack import WebClient
import requests
import json
from markdownTable import markdownTable
from random import randint
from datetime import date
from dotenv import load_dotenv
from os import getenv, path, getcwd

load_dotenv()

SLACK_TOKEN = getenv("SLACK_TOKEN")
CHANNEL_NAME = getenv("CHANNEL_NAME")

USERNAMES = [
    "abdujabbor",
    "ilkhom",
    "D4uranbek",
    "diyorbek",
    "augini",
    "laziest_coder",
    "javokhir",
    "sabohat",
    "shahnaza",
]

USERS = {
    "abdujabbor": "Abdujabbor",
    "ilkhom": "Ilkhom",
    "D4uranbek": "Davronbek",
    "augini": "Farrukh",
    "laziest_coder": "Jasurbek",
    "javokhir": "Javokhir",
    "sabohat": "Sabohat",
    "diyorbek": "Diyorbek",
    "shahnaza": "Shahnoza",
}

API_URL = "https://binarysearch.com/api"


def get_user_data():
    res = []

    for user in USERNAMES:
        r = requests.get(f"{API_URL}/users/{user}/profile")
        json_format = r.json()

        stat_data = json_format["user"]["stat"]
        solved_today = json_format["user"]["solvedToday"]

        experience_list = json_format["profile"]["experience"]

        experience_gained_today = [
            x for x in experience_list if x["date"] == date.today().strftime("%Y-%m-%d")
        ]

        if len(experience_gained_today) > 0:
            exp_gained_today = experience_gained_today[0]["gain"]
        else:
            exp_gained_today = "No gain today"

        data = {
            "Member": USERS[user],
            "Today": solved_today,
            "Exp Gained Today": exp_gained_today,
            "Overall Solved": stat_data["numTotalSolved"],
            "Streak": stat_data["streak"],
            "X": "",
        }

        res.append(data)

    sorted_res = sorted(res, key=lambda d: d["Today"], reverse=True)
    length = len(sorted_res)

    for i in range(length):
        if sorted_res[i]["Today"] != 0:
            if i == 0:
                sorted_res[i]["X"] = "🏆"
            elif i == 1:
                sorted_res[i]["X"] = "🔥"
            elif i == 2:
                sorted_res[i]["X"] = "🥉"
            else:
                sorted_res[i]["X"] = "🎉"
        else:
            random = ["📌", "📢", "🧨", "⏰", "🙀", "😲"]
            selected = random[randint(1, 5)]
            sorted_res[i]["Today"] = f"{random[1]}"
            sorted_res[i]["X"] = f"{selected}"

    return sorted_res


def send_update_on_slack():
    client = WebClient(token=SLACK_TOKEN)

    data = get_user_data()

    __location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))

    f = open(path.join(__location__, "quotes.json"))
    quotes = json.load(f)
    quote_of_today = quotes[randint(1, 10)]

    client.chat_postMessage(
        channel=CHANNEL_NAME,
        text=f"Quote of the day: \n \n{quote_of_today['quote']} ~ {quote_of_today['author']}",
    )

    client.chat_postMessage(
        channel=CHANNEL_NAME,
        text=f"Status update on {date.today()}.",
    )

    client.chat_postMessage(
        channel=CHANNEL_NAME,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{markdownTable(data).setParams(row_sep = 'always', padding_width = 5, padding_weight='center').getMarkdown()}",
                },
            }
        ],
    )


if __name__ == "__main__":
    send_update_on_slack()
