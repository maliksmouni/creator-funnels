# CLAUDE.md

Repo für Creator-Funnels. Ablauf und Regeln stehen im Skill `.claude/skills/creator-funnel/SKILL.md`.

## Creator-/Lead-Listen

Whenever the user asks for a creator or lead list ("find creators", "new list", "10 leads" …), follow `_shared/lead-search/README.md` step by step, including step 2 (`find_ig.py` for channels that don't link Instagram on YouTube) and the exclusion of everyone on earlier lists. Use the parameters from the user's request; defaults are in the README prompt. The Apify token comes from the `APIFY_TOKEN` environment variable.

## Outreach-E-Mail nach dem Livegang

After every funnel is live and verified, create a Gmail **draft** (never send it) to the creator's email address using the email template below. Replace {Name} with the creator's first name and {Nische} with their niche in one or two words. Put the placeholder line `>>> PASTE LINK HERE <<<` where {Link} goes. The user pastes the link and sends the draft themselves.

- Why no sending and no link in the draft: the Gmail connector rewrites every URL (plain text, HTML, bare domains, drafts) to an unsigned `https://www.google.com/url?q=…` link, and clicking it shows Google's "Redirect notice" warning page instead of the funnel (tested 28.09.2026). A link pasted by hand in Gmail works normally.
- At the very end of the reply for each finished funnel, show the pitch link on its own line in a code block for easy copy and paste, e.g.

  ```
  https://infooperate.pages.dev/{slug}/
  ```

  and say that the draft is waiting in Gmail → Drafts.
- Also send the user `{slug}/assets/story.jpg` (the Instagram story, made by `_shared/thumbs.mjs`) as a file, with these steps: upload as a story, add a link sticker with the pitch link under "Tap the link", add a mention sticker `@{creator handle}`, share to **Close Friends** (creator on the list). Posting is always done by the user in the app.
- Right after the story image, show the creator's Instagram profile link on its own line as a **clickable link, not in a code block** (the user taps it on mobile to open the profile and add them to Close Friends), e.g.

  [instagram.com/{handle}](https://www.instagram.com/{handle}/)

  Order at the end of the reply: story image + steps → Instagram profile link → pitch link.
- "Live and verified" means: Phase 8 of the skill passed (all pages 200 on the live site, private files 404).
- The link is the pitch page `https://infooperate.pages.dev/{slug}/`, not the funnel. No workers.dev address, no tracking link.
- Use only an email address the creator publishes themselves (bio, website, YouTube "About") or one the user gives. Record where it came from in `{slug}/README.md`.
- If the Gmail connector isn't available in the session, say so and hand over the finished email text (with the real link) instead.

Template:

```
Subject: {Name}, I've built you something

Hey {Name},

Your {Nische} content is clearly working, but I'd guess a lot of followers never make it from watching to buying.

I built you a complete call funnel to fix that:

{Link}

I recently helped Karl Pierre generate 10K in 2 days, and another creator did 6K in 8 days.

I work on a performance basis. Let me know if you want to implement this.

Malik Alexander Smouni
```
