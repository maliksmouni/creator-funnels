# CLAUDE.md

Repo für Creator-Funnels. Ablauf und Regeln stehen im Skill `.claude/skills/creator-funnel/SKILL.md`.

## Creator-/Lead-Listen

Whenever the user asks for a creator or lead list ("find creators", "new list", "10 leads" …), follow `_shared/lead-search/README.md` step by step, including step 2 (`find_ig.py` for channels that don't link Instagram on YouTube) and the exclusion of everyone on earlier lists. Use the parameters from the user's request; defaults are in the README prompt. The Apify token comes from the `APIFY_TOKEN` environment variable.
For German creators ("German", "deutsche", "DACH" …) use the README section "German creators (DACH)"; funnels for them are built in German with "du" (skill section "Deutsche Creator").

## Outreach-E-Mail nach dem Livegang

After every funnel is live and verified, create a Gmail **draft** (never send it) to the creator's email address using the email template below. Replace {Name} with the creator's first name and fill {Angebot} and {Beobachtung} as described below the template. The follow-up draft comes later (section "Follow-up"). Put the placeholder line `>>> PASTE LINK HERE <<<` where {Link} goes. The user pastes the link and sends the draft themselves.

- Why no sending and no link in the draft: the Gmail connector rewrites every URL (plain text, HTML, bare domains, drafts) to an unsigned `https://www.google.com/url?q=…` link, and clicking it shows Google's "Redirect notice" warning page instead of the funnel (tested 28.09.2026). A link pasted by hand in Gmail works normally.
- At the very end of the reply for each finished funnel, show the pitch link on its own line in a code block for easy copy and paste, e.g.

  ```
  https://infooperate.com/{slug}/
  ```

  and say that the draft is waiting in Gmail → Drafts.
- Also send the user `{slug}/assets/story.jpg` (the Instagram story, made by `_shared/thumbs.mjs`) as a file, with these steps: upload as a story, add a link sticker with the pitch link under "Tap the link", add a mention sticker `@{creator handle}`, share to **Close Friends** (creator on the list). Posting is always done by the user in the app.
- Right after the story image, show the creator's Instagram profile link on its own line as a **clickable link, not in a code block** (the user taps it on mobile to open the profile and add them to Close Friends), e.g.

  [instagram.com/{handle}](https://www.instagram.com/{handle}/)

  Order at the end of the reply: story image + steps → Instagram profile link → pitch link.
- "Live and verified" means: Phase 8 of the skill passed (all pages 200 on the live site, private files 404).
- The link is the pitch page `https://infooperate.com/{slug}/`, not the funnel. No pages.dev or workers.dev address, no tracking link. (Links sent before 07.10.2026 used `infooperate.pages.dev`, which still serves the same pages.)
- Use only an email address the creator publishes themselves (bio, website, YouTube "About") or one the user gives. Record where it came from in `{slug}/README.md`.
- If the Gmail connector isn't available in the session, say so and hand over the finished email text (with the real link) instead.

Template (since 07.10.2026; the old generic "{Name}, I've built you something" got 1 reply from 17 emails):

- **Subject**, alternate A and B per creator and record which one in `{slug}/README.md` (compare later via visit alerts and replies):
  - A: `{Name}, I built the funnel for your {Angebot}`
  - B: `{Angebot}: one thing I'd fix`
  {Angebot} = the offer exactly as in the pitch headline (`pitch.headline.mark`), e.g. "Team Take Profits mentorship", "£799 mentorship".
- **{Beobachtung}** = card 3 of "Four things I noticed" (the concrete bottleneck), rewritten as 1–2 plain sentences addressed to the creator. It is the preview line in the inbox, so it must be specific to them. No income claims.

```
Subject: (A or B, see above)

Hey {Name},

{Beobachtung}

So I built the fix: a complete call funnel for your {Angebot}, with the page, the application, the pre-call emails and the ad scripts:

{Link}

I recently helped Karl Pierre generate 10K in 2 days, and another creator did 6K in 8 days.

I work on a performance basis. Let me know if you want to implement this.

Malik Alexander Smouni
```

## Follow-up (3–4 days later, no reply)

A reply needs the first email to be sent, so at the start of each session check `in:sent subject:funnel OR subject:"built you something"` for first emails without a follow-up and create the follow-up as a Gmail draft **reply in the same thread** (`replyToMessageId` = the sent first email), so the user only sends it on the day. Tell the user the send date (first email + 3–4 days). Skip creators who already replied. Same link placeholder rule.

```
Hey {Name},

Quick follow-up on the funnel I built for your {Angebot}.

The one thing I'd change first: {Beobachtung, one sentence}

Here it is again:

>>> PASTE LINK HERE <<<

Worth a 2-minute look?

Malik
```

## Batch mode with the lead sheet ("start")

Lead sheet: Google Sheets `1FMU4LB-2l_BiKkkEGZJYZn_uoJrDWmjxb5CE6piOD9U`, tab `Leads` (needs the Google Sheets connector in the session). Column A = `x` when the funnel is live **and** the first email is in Sent. Columns B–L as in the lead sheet (Name, User Handle, Profile link, Follower, Email, Youtube link, …).

When the user says "start":
1. **Mark the last batch:** for every row without `x` whose creator already has a live funnel in the repo, search Gmail `in:sent to:{email}`. Found → write `x` in column A. Not found → leave it empty and tell the user the draft is still waiting.
2. **Follow-ups:** run the "Follow-up" section above for all sent first emails.
3. **Next batch:** take the next **2** rows from the top without `x`, without a funnel in the repo and **with an email** in column F. Skip rows without an email and list them at the end (the user can add the address from YouTube "View email address").
4. Build both funnels with the full pipeline (skill), deploy, verify, then the outreach section above (draft, story, Instagram link, pitch link). Alternate the subject A/B across creators.
5. Don't write `x` for the new batch yet. That happens at the next "start", once the emails are in Sent.

If the Sheets connector isn't available, say so and ask the user to turn it on; don't work from an old copy of the list.
