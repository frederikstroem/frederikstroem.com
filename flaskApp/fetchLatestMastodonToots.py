# A DreamHost cron job will run this every 10 minutes, (because that is the lowest interval xD).
# The output is saved to /flaskApp/latestMastodonToots.json.

import json
import requests
import re
from time import gmtime, strftime

accountId = 802809
limitDataCount = 5
apiPath = "/api/v1/accounts/{}/statuses?limit={}".format(accountId, limitDataCount)
mastodonInstance = "https://mastodon.social"
exportPath = "latestMastodonToots.json"

response = requests.get(mastodonInstance + apiPath)
if response.status_code == 200:
    dataFetchedTime = gmtime()
    dataFetchedTimeString = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    toots = json.loads(response.text)

    exportData = {
        "dataFetchedTime": dataFetchedTimeString,
        "data": [],
    }
    for toot in toots:
        exportData["data"].append({
            "date": re.sub(r'\.[0-9]*', '', toot["created_at"]),    # Regex because of speed.
            "url": toot["url"],
            "content": re.sub(r'<\/?(span|a).*?>', '', toot["content"])
        })
    with open(exportPath, 'w', encoding='utf-8') as f:
        json.dump(exportData, f, ensure_ascii=False)
