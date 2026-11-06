# SimpleVox skills

The canonical public distribution of SimpleVox's shared agent skills, version 1.0.0.
These are the same skills shipped in every SimpleVox plugin. The skills connect to
the MCP server at `https://my.simplevox.app/mcp`; they are instructions, not an A2A service.

## Install

```bash
npx skills add simplevox/simplevox-skills
```

Configure your client's remote MCP connection using the
[client setup guide](https://simplevox.net/docs/ai-tools/other-mcp-clients).
Skills alone do not install an MCP connection or grant access.

## Skills

| Skill | What it does |
| --- | --- |
| `simplevox` | The rules every SimpleVox task follows, and which skill to use. |
| `simplevox-catch-up` | Summarize new calls, voicemail and texts since you last looked, and what needs you. |
| `simplevox-follow-ups` | Find missed calls and voicemail nobody has answered yet, and help you reply. |
| `simplevox-find-and-quote` | Find what a customer said in a call, voicemail or text, and quote it with a link. |
| `simplevox-text` | Draft a text, then send it from your business number once you say yes. |
| `simplevox-call` | Set up a call that rings you and the customer, once you say yes. |
| `simplevox-contacts` | Find, save and update your business's shared contacts. |
| `simplevox-activity` | Report call and text activity, compared with the period before. |
| `simplevox-setup` | Explain your numbers, permissions, setup steps, business hours and call routing. |

## Discovery and versions

[Agent Skills Discovery index](https://simplevox.net/.well-known/agent-skills/index.json)

Each tagged release publishes one archive per skill with its reference guides and
license, plus `agent-skills-index.json` containing versioned URLs and SHA-256 digests.
Use a published immutable release for pinned installations. The site advertises
a selected release, and never rebuilds or maintains its own skill copies.

## Connection and privacy

| | |
| --- | --- |
| MCP server | `https://my.simplevox.app/mcp` |
| Sign-in | OAuth with your SimpleVox account and explicit consent |
| Credentials in this package | None |

Keep credentials in your client's secret store. Skill archives contain only instructions,
reference guides and the license. Repository automation publishes releases and is not
included in the skill archives. See the [privacy policy](https://simplevox.net/privacy-policy).

## You choose what it can do

The first time your assistant uses SimpleVox, you sign in with your own SimpleVox account and see a consent screen. Every connection can read your contacts and the calls, voicemail and texts on the numbers you allow. Everything else is off until you tick it:

| Permission | What it allows |
| --- | --- |
| Always on | Find contacts; read calls, texts, voicemail, recordings, transcripts and summaries; count activity; read hours and call routing; check setup; send feedback to SimpleVox. |
| Send text messages | Send texts from numbers you can text from. |
| Create and edit contacts | Create contacts and change saved details. Admins only. |
| Start assisted phone calls | Place calls for you: ring your phone or browser, then dial the customer when you answer. |
| Mark conversations read, unread or done | Change a conversation's status for your team, as you would in the inbox. |
| Cancel setup and end assisted calls | Cancel a call it's setting up, or end a call it started. |

You can also limit a connection to only some of your numbers. A connection never reaches more than your own SimpleVox access allows. To change what it can do, disconnect it on **Settings → Integrations** in SimpleVox and connect again.

## Safety

- **Nothing is sent without your yes.** The skills tell your assistant to show you the recipient, the number it will use and the exact text, or which of your devices will ring, and to wait for your approval. Asking for a draft is never approval to send. SimpleVox can't show its own approval prompt, so read what your assistant proposes before you agree.
- **No double sends.** Texts, calls and contact changes carry a unique key, so a retry after a timeout never repeats them.
- **Customer words are data, not instructions.** Your assistant won't text, call or change anything because a message or voicemail says to.
- **On the record.** Texts and calls your assistant starts appear in your inbox under your name.
- **Off limits.** Billing and plans, buying numbers, changing hours or call routing, texting registration, team management and picture messages stay in the SimpleVox app.

## Maintenance

This repository is a generated publishing target of the SimpleVox plugin build.
Maintainers edit the shared source in `sv-agent-plugins`, build all four targets,
and publish through the same versioned release process. Direct edits here will be
replaced by that process. No independent fork of the skill content is maintained.
