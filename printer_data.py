import sys
from datetime import timedelta, datetime
import time

from numpy import random
import requests

# Target temperatures in C
hotend_t = 220
bed_t = 90
air_t = 70

# Connection info
write_url = 'http://localhost:9092/write?db=taskk_ZfZRtYQ6RrjZohUAY9fWtG&rp=autogen&precision=s'
measurement = 'temps'


def temp(target, sigma):
    """
    Pick a random temperature from a normal distribution
    centered on target temperature.
    """
    return random.normal(target, sigma)


def main():
    session = requests.Session()
    hotend_sigma = 0
    bed_sigma = 0
    air_sigma = 0
    hotend_offset = 0
    bed_offset = 0
    air_offset = 0

    # Define some anomalies by changing sigma at certain times
    # list of sigma values to start at a specified iteration
    hotend_anomalies = [
        (0, 0.5, 0),  # normal sigma
        (3600, 3.0, -1.5),  # at one hour the hotend goes bad
        (3900, 0.5, 0),  # 5 minutes later recovers
    ]
    bed_anomalies = [
        (0, 1.0, 0),  # normal sigma
        (28800, 5.0, 2.0),  # at 8 hours the bed goes bad
        (29700, 1.0, 0),  # 15 minutes later recovers
    ]
    air_anomalies = [
        (0, 3.0, 0),  # normal sigma
        (10800, 5.0, 0),  # at 3 hours air starts to fluctuate more
        (43200, 15.0, -5.0),  # at 12 hours air goes really bad
        (45000, 5.0, 0),  # 30 minutes later recovers
        (72000, 3.0, 0),  # at 20 hours goes back to normal
    ]

    # Start from 2016-01-01 00:00:00 UTC
    # This makes it easy to reason about the data later
    now = datetime(2016, 1, 1)
    second = timedelta(seconds=1)
    epoch = datetime(1970, 1, 1)

    # 24 hours of temperatures once per second
    for i in range(60 * 60 * 24 + 2):
        # update sigma values
        if len(hotend_anomalies) > 0 and i == hotend_anomalies[0][0]:
            hotend_sigma = hotend_anomalies[0][1]
            hotend_offset = hotend_anomalies[0][2]
            hotend_anomalies = hotend_anomalies[1:]

        if len(bed_anomalies) > 0 and i == bed_anomalies[0][0]:
            bed_sigma = bed_anomalies[0][1]
            bed_offset = bed_anomalies[0][2]
            bed_anomalies = bed_anomalies[1:]

        if len(air_anomalies) > 0 and i == air_anomalies[0][0]:
            air_sigma = air_anomalies[0][1]
            air_offset = air_anomalies[0][2]
            air_anomalies = air_anomalies[1:]

        # generate temps
        hotend = temp(hotend_t + hotend_offset, hotend_sigma)
        bed = temp(bed_t + bed_offset, bed_sigma)
        air = temp(air_t + air_offset, air_sigma)
        point = "%s hotend=%f,bed=%f,air=%f %d" % (
            measurement,
            hotend,
            bed,
            air,
            time.time()
        )
        time.sleep(1)
        r = session.post(write_url, data=point)
        print(i)
        if r.status_code != 204:
            print(r.text, file=sys.stderr)
            return 1
    return 0


if __name__ == '__main__':
    exit(main())
