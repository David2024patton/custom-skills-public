# Rejected Source Media in Social Publishing

## Separate the layers of approval

- Treat source media, treatment and copy as three separate approvals. Approval of a template, frame, caption style or render approves only that layer.

- Treat a rejection of source footage or an image as a rejection of that asset in every later render. Re-dressing, re-cropping, re-captioning or re-rendering the same source does not clear the rejection.

- Treat silence about a source as no approval. A source the user has not seen and approved stays unapproved even when the finished style around it is approved.

## Check the source before publishing

- Identify the source asset behind every final render before scheduling or publishing, by clip or file, not by the finished post alone.

- Compare that source against every rejection the user gave for the current series or campaign. Stop and ask when the source matches a rejected asset or when its approval status is unclear.

- Hold or cancel scheduled posts and queued runs that reuse a rejected source. Tell the user which destinations still hold that source and which ones only the user can delete in the app.

## Available connectors

- [Facebook](/opt/hatch/connectors/facebook_cli/CONNECTOR.md) for Page drafts, posts and scheduling, where a held post often still sits in the native schedule.

- [Instagram](/opt/hatch/connectors/instagram/CONNECTOR.md) for feed posts and reels, where a published post may only be removable in the app.

- [Threads](/opt/hatch/connectors/threads/CONNECTOR.md) for text and media posts published from the same approved asset.

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Keep a short rejected asset list beside the campaign plan, naming each rejected clip or image and the date the user rejected it, so later renders check one list instead of relying on memory.

- Show the user the source clip itself, not only a finished frame, when a new treatment reuses footage from an earlier round.
