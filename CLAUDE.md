# CLAUDE.md

Repo für Creator-Funnels. Ablauf und Regeln stehen im Skill `.claude/skills/creator-funnel/SKILL.md`.

## Outreach-E-Mail nach dem Livegang

After every funnel is live and verified, send the email via Gmail to the creator's email address using the email template below. Replace {Name} with the creator's first name, {Nische} with their niche in one or two words, and {Link} with the pitch page URL. If you don't have their email address, create a Gmail draft instead and tell me.

- "Live and verified" means: Phase 8 of the skill passed (all pages 200 on the live site, private files 404).
- {Link} is the pitch page, e.g. `https://infooperate.pages.dev/{slug}/`, not the funnel. Write it as the plain URL in the plain-text body (no redirect or tracking link, no workers.dev address). Gmail's own `google.com/url?q=` wrapper when a message is viewed in Gmail can't be turned off by the sender.
- Use only an email address the creator publishes themselves (bio, website, YouTube "About"). Record where it came from in `{slug}/README.md`.
- If the Gmail connector isn't available in the session, say so and hand over the finished email text instead.

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
