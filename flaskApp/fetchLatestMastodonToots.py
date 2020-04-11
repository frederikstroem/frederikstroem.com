# A DreamHost cron job will run this every 10 minutes, (because that is the lowest interval xD).
# The output is saved to /flaskApp/latestMastodonToots.json.

import os
import json
import requests
import re
from time import gmtime, strftime

accountId = 217763
limitDataCount = 5
limitDataCountFetch = 50
apiPath = "/api/v1/accounts/{}/statuses?limit={}".format(accountId, limitDataCountFetch)
mastodonInstance = "https://fosstodon.org"
exportPath = os.path.dirname(os.path.realpath(__file__)) + "/latestMastodonToots.json"  # Source: https://stackoverflow.com/a/9350788 (2020-02-24).

def trimToots(toots):
    trimmedToots = []
    count = 0
    while len(trimmedToots) < limitDataCount:
        if toots[count]["in_reply_to_id"] is None or int(toots[count]["in_reply_to_account_id"]) == accountId:
            trimmedToots.append(toots[count])
        count += 1

    return trimmedToots

response = requests.get(mastodonInstance + apiPath)
if response.status_code == 200:
    dataFetchedTime = gmtime()
    dataFetchedTimeString = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    toots = trimToots(json.loads(response.text))

    exportData = {
        "dataFetchedTime": dataFetchedTimeString,
        "data": [],
    }
    for toot in toots:
        mediaAttached = False
        if int(len(toot["media_attachments"])) > 0:
            mediaAttached = True

        exportData["data"].append({
            "date": re.sub(r'\.[0-9]*', '', toot["created_at"]),    # Regex because of speed.
            "url": toot["url"],
            "content": re.sub(r'<\/?(span|a).*?>', '', toot["content"]),
            "mediaAttached": mediaAttached
        })
    with open(exportPath, 'w', encoding='utf-8') as f:
        json.dump(exportData, f, ensure_ascii=False)
