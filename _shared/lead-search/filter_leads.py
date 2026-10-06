#!/usr/bin/env python3
"""Filter Apify profiles to leads and collect published emails.

Usage: python3 filter_leads.py channels.jsonl profiles.json [profiles2.json ...] --min 10000 --max 30000
         --ig-since 2026-09-06 [--yt-since 2026-04-06] > review.json
Logs every checked handle to checked_handles.tsv (so later runs skip it), prints funnel stats to stderr
and writes the remaining leads as JSON for review. Remove brands/companies/duplicates by hand, then
run build_xlsx.py on the reviewed file.
"""
import argparse, datetime, json, os, re, subprocess, sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')
BAD = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.js', '.css', 'sentry', 'wixpress', 'example.',
       '@2x', 'domain.com', 'email.com', 'company.com', 'u003e')
SOCIAL = ('instagram.com', 'youtube.com', 'youtu.be', 'tiktok.com', 'twitter.com', 'x.com', 'facebook.com',
          'discord', 't.me', 'linkedin', 'spotify', 'amazon', 'whop.com', 'threads.net', 'patreon')
HUBS = ('linktr.ee', 'beacons.ai', 'bio.site', 'openup.to', 'link.me', 'shor.by', 'bit.ly', 'stan.store', 'solo.to')


def get(u):
    return subprocess.run(['curl', '-s', '-L', '--max-time', '20', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128', u],
                          capture_output=True, text=True, errors='ignore').stdout


def emails(t):
    t = t.replace('&#64;', '@').replace('%40', '@').replace('\\u0040', '@')
    return {e.lower().rstrip('.') for e in EMAIL.findall(t) if not any(b in e.lower() for b in BAD)}


def find_emails(u, ch):
    found = {}
    for e in emails(u.get('biography') or ''):
        found.setdefault(e, 'Instagram bio')
    for e in ch.get('emails') or []:
        found.setdefault(e, 'YouTube channel description')
    urls = [x.get('url') for x in u.get('externalUrls') or [] if x.get('url')]
    urls += [l if l.startswith('http') else 'https://' + l for l in ch.get('links') or []]
    sites = set()
    for url in urls:
        if any(s in url for s in SOCIAL):
            continue
        for e in emails(get(url)):
            found.setdefault(e, 'Website ' + url.split('://')[-1][:60])
        host = urlparse(url).netloc
        if host and not any(h in host for h in HUBS):
            sites.add(host)
    for host in sites:
        for page in ('contact', 'contact-us', 'about', 'privacy-policy', 'terms'):
            for e in emails(get(f'https://{host}/{page}')):
                found.setdefault(e, f'Website {host}/{page}')
    return found


p = argparse.ArgumentParser()
p.add_argument('channels')
p.add_argument('profiles', nargs='+')
p.add_argument('--min', type=int, required=True)
p.add_argument('--max', type=int, required=True)
p.add_argument('--ig-since', required=True, help='earliest Instagram post date, YYYY-MM-DD')
p.add_argument('--yt-since', default='0000')
a = p.parse_args()

ch = {}
for l in open(a.channels):
    r = json.loads(l)
    if r['ig']:
        ch.setdefault(r['ig'][0].split('/')[0].lower(), r)
today = datetime.date.today().isoformat()
stats = {'profiles': 0, 'in_range': 0, 'posted_recently': 0}
leads = []
with open(os.path.join(HERE, 'checked_handles.tsv'), 'a') as log:
    for f in a.profiles:
        for u in json.load(open(f)):
            if not u.get('username'):
                continue
            stats['profiles'] += 1
            h = u['username'].lower()
            n = u.get('followersCount')
            ps = [x['timestamp'][:10] for x in u.get('latestPosts') or [] if x.get('timestamp')]
            last = max(ps) if ps else ''
            log.write(f'{h}\t{n}\t{last}\t{today}\n')
            if n is None or not a.min <= n <= a.max:
                continue
            stats['in_range'] += 1
            c = ch.get(h, {})
            if last < a.ig_since or (c.get('last_upload') or '') < a.yt_since:
                continue
            stats['posted_recently'] += 1
            leads.append({'name': u.get('fullName') or h, 'handle': h, 'followers': n, 'last_ig_post': last,
                          'youtube': c.get('yt'), 'location': c.get('country'), 'last_yt_upload': c.get('last_upload'),
                          'category': u.get('businessCategoryName'), 'bio': u.get('biography'),
                          'emails_found': find_emails(u, c), 'email': '', 'email_source': '', 'notes': ''})
            print(f'  {h}: {n} followers, emails {list(leads[-1]["emails_found"])}', file=sys.stderr)
print(stats, file=sys.stderr)
json.dump(leads, sys.stdout, indent=1, ensure_ascii=False)
