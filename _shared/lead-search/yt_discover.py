#!/usr/bin/env python3
"""Find YouTube channels for search queries and record country, Instagram, emails and last upload.

Usage: python3 yt_discover.py channels.jsonl "forex trading" "v:day trading" ...
  plain query  -> channel search results
  "v:" prefix  -> video results uploaded this month (finds smaller, active creators)
Appends one JSON line per new channel; channels already in the file are skipped.
"""
import html, json, re, subprocess, sys, urllib.parse

EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')


def get(url):
    return subprocess.run(['curl', '-s', '-L', '--max-time', '30', '-A', 'Mozilla/5.0',
                           '-H', 'Accept-Language: en-US', '-b', 'CONSENT=YES+1', url],
                          capture_output=True, text=True, errors='ignore').stdout


def search(q):
    if q.startswith('v:'):
        s = get('https://www.youtube.com/results?search_query=' + urllib.parse.quote(q[2:]) + '&sp=CAISBAgEEAE%253D')
        ids = re.findall(r'"browseId":"(UC[\w-]{22})"', s)
    else:
        s = get('https://www.youtube.com/results?search_query=' + urllib.parse.quote(q) + '&sp=EgIQAg%253D%253D')
        ids = re.findall(r'"channelId":"(UC[\w-]{22})"', s)
    return list(dict.fromkeys(ids))


def about(cid):
    a = get(f'https://www.youtube.com/channel/{cid}/about')
    r = {'cid': cid}
    m = re.search(r'"country":"([^"]*)"', a); r['country'] = m and m.group(1)
    m = re.search(r'"canonicalBaseUrl":"/(@[^"]*)"', a)
    r['yt'] = 'https://www.youtube.com/' + (m.group(1) if m else 'channel/' + cid)
    m = re.search(r'<meta property="og:title" content="([^"]*)"', a); r['title'] = m and html.unescape(m.group(1))
    m = re.search(r'"subscriberCountText":"([^"]*)"', a); r['subs'] = m and m.group(1)
    r['links'] = [l.replace('\\u0026', '&') for l in re.findall(
        r'channelExternalLinkViewModel":\{"title":\{"content":"[^"]*"\},"link":\{"content":"([^"]*)"', a)]
    m = re.search(r'"description":"((?:[^"\\]|\\.)*)"', a)
    desc = json.loads('"' + m.group(1) + '"') if m else ''
    ig = [l for l in r['links'] if 'instagram.com' in l] + re.findall(r'instagram\.com/[A-Za-z0-9._]+', desc)
    r['ig'] = [re.sub(r'.*instagram\.com/', '', x).split('?')[0].split('/')[0].lower() for x in ig]
    r['emails'] = sorted({e for e in EMAIL.findall(desc) if not e.endswith(('.png', '.jpg'))})
    rss = get(f'https://www.youtube.com/feeds/videos.xml?channel_id={cid}')
    dates = re.findall(r'<entry>.*?<published>([^<]*)', rss, re.S)
    r['last_upload'] = max(dates)[:10] if dates else None
    return r


if __name__ == '__main__':
    out = sys.argv[1]
    try:
        seen = {json.loads(l)['cid'] for l in open(out)}
    except FileNotFoundError:
        seen = set()
    for q in sys.argv[2:]:
        new = 0
        for cid in search(q):
            if cid in seen:
                continue
            seen.add(cid)
            try:
                r = about(cid)
            except Exception:
                continue
            r['query'] = q
            with open(out, 'a') as f:
                f.write(json.dumps(r) + '\n')
            new += 1
        print(f'{q}: {new} new channels', flush=True)
