import csv
import json
from redis import Redis
import time

redis = Redis(host="redis", port=6379)

data = {}

with open("airports.csv", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
    count = 0
    for row in spamreader:
        if not row[13] or count == 0:
            count += 1
            continue
        count += 1
        data[row[13]] = json.dumps(
            {
                "id": row[0],
                "type": row[2],
                "name": row[3],
                "iso_country": row[8],
                "iso_region": row[9],
                "iata_code": row[13],
            }
        )
    print(count)

for key, value in data.items():
    time.sleep(.01)
    print(redis.set(key, value))
