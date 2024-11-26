#!/usr/bin/env python3
# pylint: disable=invalid-name
""" BOM """
# -*- coding: utf-8 -*-
# <bitbar.title>BOM Scoresby Current Temperature</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Andrew Duncan</bitbar.author>
# <bitbar.desc>Displays current temperature from BOM website</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import datetime
import json
import urllib.request

try:
    url = 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95867.json'
    with urllib.request.urlopen(url) as response:
        data = response.read().decode(response.info().get_param('charset') or 'utf-8')
    json = json.loads(data)

    observations = json['observations']
    header = observations['header'][0]
    data = observations['data']
    latest = data[0]

    if latest['air_temp'] is None:
        print("bom | color='orange' size=11")
    else:
        print(f"{latest['air_temp']}°C | size=11")

    print("---")

    bom_url = "http://www.bom.gov.au/vic/observations/melbourne.shtml?ref=hdr"

    print(f"{header['refresh_message']} | color='black' href='{bom_url}'")
    print(f"Location: {header['name']} | color='black' href='{bom_url}'")

    wind_dir = latest['wind_dir']

    if wind_dir is None:
        print(f"Wind: ???? | color='black' href='{bom_url}'")
    elif wind_dir == "CALM":
        print(f"Wind: calm | color='black' href='{bom_url}'")
    else:
        print(f"Wind: {latest['wind_dir']} - "
              f"{latest['wind_spd_kt']} kts gusting to {latest['gust_kt']} kts "
              f"| color='black' href='{bom_url}'")

    print("---")

    now = datetime.datetime.now()
    local_now = now.astimezone()
    local_tz = local_now.tzinfo
    local_tzname = local_tz.tzname(local_now)
    retrieved = now.strftime("%-I:%M %p ") + local_tzname + now.strftime(" %A %e %B %Y")
    print(f"Retrieved at {retrieved}| color='black' size=10 href='{bom_url}'")

except Exception as exception:  # pylint: disable=broad-except

    print("bom | color='gray' size=11")
    print("---")
    print(exception)
