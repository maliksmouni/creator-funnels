#!/usr/bin/env python3
"""Fetch Instagram profiles through Apify (apify/instagram-profile-scraper). Never call Instagram directly.

Usage: python3 apify_ig.py handles.txt profiles.json
APIFY_TOKEN must be set in the environment (cloud environment settings). Prints the run cost and this month's Apify usage.
"""
import json, os, subprocess, sys

token = os.environ.get('APIFY_TOKEN') or sys.exit('APIFY_TOKEN is not set: add it in the cloud environment settings (environment menu -> Edit).')
handles = open(sys.argv[1]).read().split()
body = json.dumps({'usernames': handles})
res = subprocess.run(['curl', '-s', '--max-time', '900', '-X', 'POST', '-H', 'Content-Type: application/json',
                      '-H', f'Authorization: Bearer {token}', '-d', body,
                      'https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items'],
                     capture_output=True, text=True).stdout
data = json.loads(res)
json.dump(data, open(sys.argv[2], 'w'))
print(f'{len(data)} profiles for {len(handles)} handles')
for url, key in (('https://api.apify.com/v2/acts/apify~instagram-profile-scraper/runs?desc=1&limit=1', 'run'),
                 ('https://api.apify.com/v2/users/me/limits', 'limits')):
    d = json.loads(subprocess.run(['curl', '-s', '-H', f'Authorization: Bearer {token}', url],
                                  capture_output=True, text=True).stdout)['data']
    if key == 'run':
        print(f"run cost: ${d['items'][0].get('usageTotalUsd') or 0:.3f}")
    else:
        print(f"Apify usage this month: ${d['current']['monthlyUsageUsd']:.2f} of ${d['limits']['maxMonthlyUsageUsd']}")
