from slack import WebClient
import requests

from markdownTable import markdownTable
from random import randint
from datetime import date
from dotenv import load_dotenv
from os import getenv

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
        data = {
            "Member": USERS[user],
            "Today": solved_today,
            "Easy": stat_data["numEasySolvedToday"],
            "Medium": stat_data["numMediumSolvedToday"],
            "Hard": stat_data["numHardSolvedToday"],
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

    client.chat_postMessage(
        channel=CHANNEL_NAME,
        text=f"BinarySearch Status on {date.today()}. Let's keep coding!",
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
