"""Does an Instagram handle/profile belong to a YouTube channel? Shared by find_ig.py and filter_leads.py."""
import re

GENERIC = {'trading', 'trader', 'traders', 'trades', 'trade', 'official', 'the', 'and', 'with', 'forex', 'stocks',
           'stock', 'options', 'futures', 'crypto', 'day', 'daytrading', 'fx', 'tv', 'live', 'channel', 'academy',
           'invest', 'investing', 'market', 'markets', 'money', 'capital', 'real', 'mr', 'its'}


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def tokens(s):
    return {t for t in re.findall(r'[a-z0-9]+', (s or '').lower()) if len(t) >= 4 and t not in GENERIC}


def resembles(handle, title, yt_url):
    """Handle looks like the channel: same normalized name, or shares a distinctive word."""
    h = norm(handle)
    yt = norm(re.sub(r'.*/@', '', yt_url or ''))
    t = norm(title)
    if h and (h == yt or h == t or (len(h) >= 5 and (h in yt or yt in h or h in t))):
        return True
    return any(tok in h for tok in tokens(title) | tokens(re.sub(r'.*/@', '', yt_url or '')))


def matches_channel(profile, channel):
    """Instagram profile (Apify) links this YouTube channel, or carries the channel's name."""
    links = ' '.join([profile.get('biography') or ''] + [x.get('url') or '' for x in profile.get('externalUrls') or []]).lower()
    yt_handle = re.sub(r'.*/@', '', channel.get('yt') or '').lower()
    if channel.get('cid', '').lower() in links or (yt_handle and '@' + yt_handle in links.replace('youtube.com/', '@').replace('@@', '@')):
        return True
    if norm(profile.get('fullName')) and norm(profile.get('fullName')) in (norm(channel.get('title')),):
        return True
    return bool(tokens(profile.get('fullName')) & tokens(channel.get('title')))
