# Lead search (internal, never deployed)

Finds creators for outreach: YouTube first, Instagram checked through Apify, only emails the creators publish themselves.
`_shared/` is blocked on every host (Netlify `_redirects`, Cloudflare `publish.py` allowlist, `functions/_middleware.js`).

| File | Purpose |
|---|---|
| `yt_discover.py` | YouTube search → channel country, Instagram link, emails, last upload (free, no key) |
| `find_ig.py` | Finds Instagram for channels that don't link it on YouTube (~70%): from their website/link page, else a same-name guess that `filter_leads.py` verifies |
| `match.py` | Decides whether an Instagram profile belongs to a YouTube channel (shared helper) |
| `candidates.py` | Instagram handles to check: country + active + Instagram linked, minus exclusions |
| `apify_ig.py` | Instagram profiles via Apify (`APIFY_TOKEN` env), prints run cost + monthly usage |
| `filter_leads.py` | Follower range + post dates, collects published emails, logs every checked handle |
| `build_xlsx.py` | Writes the lead sheet (clickable links, missing emails yellow) |
| `exclude_handles.txt` | Everyone already on a lead list. `build_xlsx.py` appends each run's leads automatically; add same-person pairs by hand |
| `checked_handles.tsv` | Every handle already checked on Apify (followers, last post, date). Skipped for 90 days (`--recheck-days`), then checked again because followers change |

Lead sheets themselves (with emails) are not committed; they go to the user as a file.

## Reusable prompt

Copy this into a new session, edit the parameters and attach any lead sheets to skip. The Apify token comes from the `APIFY_TOKEN` variable in the cloud environment settings (environment menu in the session title bar → Edit); never paste it into the chat.

```
Build me a creator lead list with the lead search in _shared/lead-search/ (read its README first and follow it).

Parameters:
- Niche: trading (day trading, forex, futures, options)
- Countries: United States, United Kingdom
- Instagram followers: 10,000–30,000
- Instagram: at least one post in the last 30 days
- YouTube: channel required, at least one upload in the last 6 months
- Number of leads: 10
- Exclude: attached sheet(s) + exclude_handles.txt + checked_handles.tsv
- Apify token: already set as APIFY_TOKEN in the environment (if it's missing, stop and tell me)

When done: commit the updated exclude_handles.txt and checked_handles.tsv (never the token or the lead sheet),
send me the .xlsx, and report as described in the README.
```

## Method

Scratch files (channels.jsonl, handles, profiles, review.json) go in the session scratchpad, not the repo.

1. **Discover** with many varied queries (strategies, markets, formats like "vlog", "live trading", "prop firm", "recap"). Mix channel search and `v:` video search (videos from this month find smaller, active creators). Results repeat quickly, so keep adding new angles; earlier runs used ~110 trading/forex/crypto queries, so look for new ones.
   `python3 yt_discover.py $S/channels.jsonl "query" "v:query" ...`
2. **Find missing Instagram handles**: `python3 find_ig.py $S/channels.jsonl --since <YouTube window date>`. Adds handles for channels that don't link Instagram on YouTube: trusted when the creator's own website/link page links an account resembling the channel, otherwise marked for verification. `filter_leads.py` drops any unverified handle whose Instagram profile neither links the YouTube channel nor carries its name (sponsors such as TradingView or prop firms often appear on creators' sites). In the test this turned 0 remaining candidates into 287.
3. **Candidates** (skips everyone on an earlier list, every creator with a funnel in this repo, and accounts checked in the last 90 days): `python3 candidates.py $S/channels.jsonl --since <YYYY-MM-DD, YouTube window> --exclude <attached.xlsx> > $S/handles.txt`
   Rule of thumb: ~130 candidates per 10 leads. If too few, go back to step 1.
   ~70% of active US/UK channels don't link Instagram on YouTube. If candidates run dry, find their Instagram via their website / link-in-bio page, or try the same handle on Instagram, and only keep it when bio, name or YouTube link confirm it's the same person.
4. **Instagram via Apify**: `python3 apify_ig.py $S/handles.txt $S/profiles1.json` (one batch can hold hundreds of handles).
   Never call Instagram directly (this server gets 429 / "please wait" blocks), no mirror sites, never a logged-in Instagram or Google account or cookies.
5. **Filter + emails**: `python3 filter_leads.py $S/channels.jsonl $S/profiles*.json --min 10000 --max 30000 --ig-since <date> --yt-since <date> > $S/review.json`
6. **Review review.json by hand** and edit it:
   - Remove brands, brokers, prop firms, academies, software, media (e.g. Topstep, IG UK, tastylive, FX Replay, London Academy of Trading), accounts whose bio says they're inactive, and people already on a list under another handle (e.g. @realbthetrader = @bthestory87; add such pairs to `exclude_handles.txt`).
   - Set `email` + `email_source` from `emails_found`, using only the creator's own address. Ignore sponsor/affiliate emails (prop firms, brokers, tools they promote) and generic legal/privacy addresses. Never guess an email; leave it empty if none fits.
   - Set a better `name` if `fullName` is a slogan, and put doubts in `notes` (e.g. bio flag suggests another country than YouTube says, community/brand-like account).
7. **Sheet**: `python3 build_xlsx.py $S/review.json $S/<niche>_leads_<date>.xlsx`, send it to the user.
8. **Commit and push** `exclude_handles.txt` (updated by `build_xlsx.py`) and `checked_handles.tsv` (updated by `filter_leads.py`). Without this push the next session would not know these creators.

## German creators (DACH)

When the user asks for German creators, run the same method with:
- **Countries:** `--countries "Germany,Austria,Switzerland"` for `candidates.py` and `find_ig.py` (YouTube reports these names in English).
- **Search:** `yt_discover.py --region DE …` with German queries, e.g. "Daytrading lernen", "Trading Strategie deutsch", "Forex Trading Anfänger", "v:Trading Vlog deutsch", "v:Prop Firm Challenge deutsch", "v:Daytrading live deutsch", plus English niche terms (many German traders use them).
- **Emails:** German sites must have an Impressum, so `filter_leads.py` also checks `/impressum`, `/kontakt` and `/datenschutz`. An Impressum email is published by the creator and can be used.
- **Sheet:** add "Language: German" in Notes. Funnels for these leads are built in German with "du" (see the funnel skill, section "Deutsche Creator").

## Report to the user

- Table of the leads with email + where it was published.
- Clickable YouTube links for leads without an email (they use "View email address" on the About page themselves; it needs a login + captcha, so it can't be automated safely).
- Funnel stats: channels found → country → active → Instagram linked → in follower range → posted recently → leads.
- Apify cost of the run and usage this month (printed by `apify_ig.py`).

## Known facts (trading test, Oct 2026)

- Apify instagram-profile-scraper: ~$0.0026 per profile. Free plan $5/month ≈ 1,900 profiles ≈ 150 leads at the hit rate below; in practice finding new YouTube channels runs out first.
- YouTube first: 129 profiles → 10 leads (~8%). Of checked profiles: 18% under 1K, 22% 1–10K, 16% 10–30K, 12% 30–100K, 22% over 100K, 9% not found.
- Follower range is the main filter. A 60-day Instagram window only raised the hit rate from ~8% to ~9%, 90 days to ~11%. Widening the follower range (e.g. 5–30K) helps much more.
- Instagram first (`apify~instagram-search-scraper`) failed: 0 leads from 171 accounts (no country filter, place names pull in unrelated accounts, few have YouTube, more expensive). Don't use it.
- Crypto: 0 leads from 22 candidates; creators skew to over 30K or brands, and channels are very international.
- About half of the leads have a published email (Instagram bio, YouTube description or own website).
