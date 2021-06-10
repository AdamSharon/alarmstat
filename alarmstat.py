import click
import requests
import json
from pprint import pprint

from datetime import datetime

# testing testing

class AlarmStats(object):
    URL = "https://www.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx"

    HEADERS = {
        "Referer": "https://www.oref.org.il/11226-he/pakar.aspx",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }

    def __init__(self, hours):
        self.hours = hours

    def fetch(self):
        res = requests.get(self.URL, headers=self.HEADERS)
        now = datetime.now()
        if res.content:            
            data = json.loads(res.content)
            filtered_data = list(filter(lambda x: (now - datetime.strptime(x['datetime'],"%Y-%m-%dT%H:%M:%S")).seconds < self.hours * 60 * 60, data))
            stats = build_stats(filtered_data)
            pprint(dict(sorted(stats.items(), key=lambda x: x[1], reverse=True)), sort_dicts=False)


def build_stats(data: list) -> dict:
    stats = {}
    for entry in data:
        city = entry['data'][::-1] # reverse the name since names are in hebrew and i want to display it pretty
        if stats.__contains__(city):
            stats[city] += 1
        else:
            stats[city] = 1
    return stats


@click.command()
@click.option("--hours", default=1, help="number of hours")
def alarm_stats(hours):
    AlarmStats(
        hours=hours
    ).fetch()

if __name__ == "__main__":
    alarm_stats() 