#!/usr/bin/env python3
"""Find Instagram handles for channels that don't link Instagram on YouTube.

Usage: python3 find_ig.py channels.jsonl [--since 2026-04-06] [--countries "United States,United Kingdom"]
Rewrites channels.jsonl in place. For each channel in the countries, active since --since and without
an Instagram handle:
  1. website: open the channel's own links (website, Linktree, Beacons, Stan, Whop ...; affiliate links
     skipped) and collect the Instagram profiles linked there. A handle that resembles the channel, or
     comes from a personal link page, is trusted -> ig_source "website". Otherwise (often a sponsor's
     account) -> "website-check".
  2. guess: no handle found -> the YouTube handle as a guess -> ig_source "guess".
filter_leads.py keeps "website-check" and "guess" only if the Instagram profile links this YouTube
channel or carries the same name (see matches_channel).
"""
import argparse, collections, json, re, subprocess
from match import norm, resembles

SKIP = ('instagram.com', 'youtube.com', 'youtu.be', 'tiktok.com', 'twitter.com', 'x.com', 'facebook.com',
        'discord', 't.me', 'linkedin', 'spotify', 'amazon', 'apple.com', 'threads.net', 'patreon')
NOT_PROFILE = {'p', 'reel', 'reels', 'explore', 'accounts', 'stories', 'tv', 'direct', 'about', 'legal',
               'developer', 'instagram', 'share', 'web', 'privacy', 'press'}
HUBS = ('linktr.ee', 'beacons.ai', 'stan.store', 'bio.site', 'solo.to', 'link.me', 'campsite.bio', 'hoo.be', 'msha.ke', 'lnk.bio')
AFFILIATE = re.compile(r'[?&](ref|refid|referral|referral_id|aff|affiliate|via|fpr|utm_[a-z]+)=|/aff/|/go/|/ref/|/partner', re.I)
IG = re.compile(r'instagram\.com/([A-Za-z0-9._]{2,30})', re.I)


def get(u):
    return subprocess.run(['curl', '-s', '-L', '--max-time', '20', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128', u],
                          capture_output=True, text=True, errors='ignore').stdout


def from_links(r):
    """Return (handle, trusted) from the channel's own links, or (None, False)."""
    found = collections.Counter()
    from_hub = set()
    for link in r['links']:
        url = link if link.startswith('http') else 'https://' + link
        if any(s in url for s in SKIP) or AFFILIATE.search(url):
            continue
        for h in IG.findall(get(url).replace('\\/', '/')):
            h = h.lower().rstrip('.')
            if h in NOT_PROFILE or re.fullmatch(r'[a-z]{2}_[a-z]{2}', h) or re.search(r'\.(js|css|php|html?|png|jpe?g|svg)$', h):
                continue
            found[h] += 1
            if any(x in url for x in HUBS):
                from_hub.add(h)
    for h, _ in found.most_common():
        if resembles(h, r['title'], r['yt']):
            return h, True
    if from_hub:
        return max(from_hub, key=found.get), True
    return (found.most_common(1)[0][0], False) if found else (None, False)


p = argparse.ArgumentParser()
p.add_argument('channels')
p.add_argument('--since', default='0000')
p.add_argument('--countries', default='United States,United Kingdom')
a = p.parse_args()
countries = set(a.countries.split(','))

rows = [json.loads(l) for l in open(a.channels)]
stats = collections.Counter()
for r in rows:
    if r['ig'] or r.get('ig_source') or r['country'] not in countries or (r['last_upload'] or '') < a.since:
        continue
    stats['looked up'] += 1
    h, trusted = from_links(r)
    if h:
        r['ig'], r['ig_source'] = [h], 'website' if trusted else 'website-check'
    else:
        guess = re.sub(r'.*/@', '', r['yt']).lower()
        if re.fullmatch(r'[a-z0-9._]{2,30}', guess) and not r['yt'].endswith(r['cid']):
            r['ig'], r['ig_source'] = [guess], 'guess'
        else:
            r['ig_source'] = 'none'
    stats[r['ig_source']] += 1
    print(f"{r['title']}: {r['ig'][0] if r['ig'] else '-'} ({r['ig_source']})", flush=True)

with open(a.channels, 'w') as f:
    for r in rows:
        f.write(json.dumps(r) + '\n')
print(dict(stats))
