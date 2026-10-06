#!/usr/bin/env python3
"""Pick Instagram handles to check from yt_discover output.

Usage: python3 candidates.py channels.jsonl --since 2026-04-06 [--countries "United States,United Kingdom"]
         [--exclude file.xlsx|file.txt ...] > handles.txt
Keeps channels in the given countries with an upload on/after --since and a linked Instagram,
minus creators already listed or pitched, so nobody lands on two lists:
  - exclude_handles.txt (every earlier lead list) and any --exclude files (xlsx: column "User Handle"; txt: first column)
  - every creator with a funnel in the repo ({slug}/content.json -> instagram, else slug)
  - checked_handles.tsv entries checked within --recheck-days (older ones are checked again, since followers change)
"""
import argparse, datetime, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))


def load_exclude(path):
    if path.endswith('.xlsx'):
        import openpyxl
        ws = openpyxl.load_workbook(path).active
        rows = list(ws.iter_rows(values_only=True))
        col = [str(c).strip().lower() for c in rows[0]].index('user handle')
        return {str(r[col]).strip().lstrip('@').lower() for r in rows[1:] if r[col]}
    return {l.split('\t')[0].strip().lstrip('@').lower() for l in open(path) if l.strip() and not l.startswith('#')}


p = argparse.ArgumentParser()
p.add_argument('channels')
p.add_argument('--since', required=True, help='earliest YouTube upload date, YYYY-MM-DD')
p.add_argument('--countries', default='United States,United Kingdom')
p.add_argument('--exclude', nargs='*', default=[])
p.add_argument('--recheck-days', type=int, default=90, help='re-check rejected handles after this many days')
a = p.parse_args()

listed = set()
for f in a.exclude + [os.path.join(HERE, 'exclude_handles.txt')]:
    if os.path.exists(f):
        listed |= load_exclude(f)
funnels = set()
for f in glob.glob(os.path.join(REPO, '*', 'content.json')):
    c = json.load(open(f))
    funnels.add((c.get('instagram') or c.get('slug') or '').lower())
cutoff = (datetime.date.today() - datetime.timedelta(days=a.recheck_days)).isoformat()
checked = set()
log = os.path.join(HERE, 'checked_handles.tsv')
if os.path.exists(log):
    for l in open(log):
        f = l.rstrip('\n').split('\t')
        if l.startswith('#') or len(f) < 4:
            continue
        if f[3] >= cutoff:
            checked.add(f[0].lower())
ex = listed | funnels | checked
print(f'excluding {len(listed)} listed, {len(funnels)} with a funnel, {len(checked)} checked in the last {a.recheck_days} days',
      file=sys.stderr)
countries = set(a.countries.split(','))
out, stats = [], {'channels': 0, 'country': 0, 'active': 0, 'instagram': 0}
for l in open(a.channels):
    r = json.loads(l)
    stats['channels'] += 1
    if r['country'] not in countries:
        continue
    stats['country'] += 1
    if not r['last_upload'] or r['last_upload'] < a.since:
        continue
    stats['active'] += 1
    if not r['ig']:
        continue
    stats['instagram'] += 1
    h = r['ig'][0].split('/')[0].lower()
    if h and h not in ex and h not in out:
        out.append(h)
print(' '.join(out))
print(stats, f'-> {len(out)} new handles', file=sys.stderr)
