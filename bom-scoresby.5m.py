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

import subprocess
import requests

try:
    req = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95867.json')

    # pylint: disable=E1101
    if req.status_code != requests.codes.ok:
        raise Exception('error from BOM', req.status_code)

    json = req.json()

    observations = json['observations']
    header = observations['header'][0]
    data = observations['data']
    latest = data[0]

    if latest['air_temp'] is None:
        print("bom | color='orange' size=11")
    else:
        print(f"{latest['air_temp']}°C | size=11")

    print("---")

    URL="http://www.bom.gov.au/vic/observations/melbourne.shtml?ref=hdr"

    print(f"{header['refresh_message']} | color='black' href='{URL}'")
    print(f"Location: {header['name']} | color='black' href='{URL}'")

    wind_dir = latest['wind_dir']

    if wind_dir is None:
        print(f"Wind: ???? | color='black' href='{URL}'")
    elif wind_dir == "CALM":
        print(f"Wind: calm | color='black' href='{URL}'")
    else:
        print(f"Wind: {latest['wind_dir']} - "
              f"{latest['wind_spd_kt']} kts gusting to {latest['gust_kt']} kts "
              f"| color='black' href='{URL}'")

    print("---")

    result = subprocess.run(['/bin/date', '+%l:%M %p %Z %A %e %B %Y'],
                            check = False,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE)
    retrieved = result.stdout.decode().rstrip()
    print(f"Retrieved at {retrieved}| color='black' size=10 href='{URL}'")

except Exception as exception:  # pylint: disable=broad-except

    print("bom | color='red' size=11")
    print("---")
    print(exception)
