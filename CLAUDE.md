# CLAUDE.md

Repo für Creator-Funnels. Ablauf und Regeln stehen im Skill `.claude/skills/creator-funnel/SKILL.md`.

## Creator-/Lead-Listen

Whenever the user asks for a creator or lead list ("find creators", "new list", "10 leads" …), follow `_shared/lead-search/README.md` step by step, including step 2 (`find_ig.py` for channels that don't link Instagram on YouTube) and the exclusion of everyone on earlier lists. Use the parameters from the user's request; defaults are in the README prompt. The Apify token comes from the `APIFY_TOKEN` environment variable.
For German creators ("German", "deutsche", "DACH" …) use the README section "German creators (DACH)"; funnels for them are built in German with "du" (skill section "Deutsche Creator").

## Outreach-E-Mail nach dem Livegang

After every funnel is live and verified, create a Gmail **draft** (never send it) to the creator's email address using the email template below. Replace {Name} with the creator's first name and fill {Angebot} and {Beobachtung} as described below the template. The follow-up draft comes later (section "Follow-up").

**Since 09.10.2026 the first email has no link.** It is plain text (no link, no image, no attachment, for the best inbox placement) and asks "Can I send you the link?", so the creator only has to reply (easier than clicking an unknown link, and replies help deliverability). The user sends the draft themselves. A preview image in the email was considered and dropped on 09.10.2026 (Promotions-tab risk). When the creator replies yes, create a reply draft in the same thread with the link placeholder `>>> PASTE LINK HERE <<<` (see "Reply with the link").

- Why no sending and no link in drafts: the Gmail connector rewrites every URL (plain text, HTML, bare domains, drafts) to an unsigned `https://www.google.com/url?q=…` link, and clicking it shows Google's "Redirect notice" warning page instead of the funnel (tested 28.09.2026). A link pasted by hand in Gmail works normally.
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

Template (since 09.10.2026: plain text, no link, reply CTA; before that the same text with the link, since 07.10.2026; the old generic "{Name}, I've built you something" got 1 reply from 17 emails):

- **Subject**, alternate A and B per creator and record which one in `{slug}/README.md` (compare later via visit alerts and replies):
  - A: `Quick question about your {Angebot}` (since 09.10.2026; reads like a business enquiry. Before: `{Name}, I built the funnel for your {Angebot}`, used for Kevin, Kyle, Ash)
  - B: `{Angebot}: one thing I'd fix`
  {Angebot} = the offer exactly as in the pitch headline (`pitch.headline.mark`), e.g. "Team Take Profits mentorship", "£799 mentorship".
- **{Beobachtung}** = card 3 of "Four things I noticed" (the concrete bottleneck), rewritten as 1–2 plain sentences addressed to the creator. It is the preview line in the inbox, so it must be specific to them. No income claims.

```
Subject: (A or B, see above)

Hey {Name},

{Beobachtung}

So I built the fix: a complete call funnel for your {Angebot}, with the page, the application, the pre-call emails and the ad scripts.

I recently helped Karl Pierre generate 10K in 2 days, and another creator did 6K in 8 days.

I work on a performance basis. Can I send you the link?

Malik Alexander Smouni
```

### Reply with the link

When a creator answers the first email (yes, send it, sure …), create a draft **reply in the same thread** right away and tell the user:

```
Hey {Name},

Here it is:

>>> PASTE LINK HERE <<<

It's built for your {Angebot}: the page, the application, the pre-call emails and the ad scripts. Have a look and let me know what you think.

Malik
```

## Follow-up (3–4 days later, no reply)

A reply needs the first email to be sent, so at the start of each session check `in:sent (subject:funnel OR subject:"built you something" OR subject:"quick question about" OR subject:"one thing I'd fix")` for first emails without a follow-up and create the follow-up as a Gmail draft **reply in the same thread** (`replyToMessageId` = the sent first email), so the user only sends it on the day. Tell the user the send date (first email + 3–4 days). Skip creators who already replied. First emails sent before 09.10.2026 had the link, so their follow-up keeps it: replace the last line with "Here it is again:", the line `>>> PASTE LINK HERE <<<` and "Worth a 2-minute look?".

```
Hey {Name},

Quick follow-up on the funnel I built for your {Angebot}.

The one thing I'd change first: {Beobachtung, one sentence}

Want me to send it over? It takes 2 minutes to look through.

Malik
```

## Batch mode with the lead sheet ("start")

Lead sheet: Google Sheets `1FMU4LB-2l_BiKkkEGZJYZn_uoJrDWmjxb5CE6piOD9U`, tab `Leads` (needs the Google Sheets connector in the session). Column A = `x` when the funnel is live **and** the first email is in Sent, `skipped` when the row has no email. Columns B–L as in the lead sheet (Name, User Handle, Profile link, Follower, Email, Youtube link, …).

When the user says "start":
1. **Mark the last batch:** for every row without `x` whose creator already has a live funnel in the repo, search Gmail `in:sent to:{email}`. Found → write `x` in column A. Not found → leave it empty and tell the user the draft is still waiting.
2. **Follow-ups:** run the "Follow-up" section above for all sent first emails.
3. **Next batch:** take the next **2** rows from the top with an empty column A and without a funnel in the repo. A row without an email in column F gets `skipped` in column A and the next row is taken instead (decision 08.10.2026). Name the skipped creators at the end.
4. Build both funnels with the full pipeline (skill), deploy, verify, then the outreach section above (draft, story, Instagram link, pitch link). Alternate the subject A/B across creators.
5. Don't write `x` for the new batch yet. That happens at the next "start", once the emails are in Sent.

**New lead lists go into the same sheet:** after `build_xlsx.py`, append the new leads below the last row of tab `Leads` (same columns B–L, column A empty, same order as in the .xlsx; read the sheet first and write only below the last filled row). Then "start" picks them up automatically. Still send the .xlsx as a backup.

If the Sheets connector isn't available, say so and ask the user to turn it on; don't work from an old copy of the list.
