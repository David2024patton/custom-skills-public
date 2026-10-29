# Google Business Profiles

## Establish which profile you are touching

- Verify the signed-in Google account is the profile owner's account before any edit, using the browser's saved-login flow and asking the owner for a 2-Step Verification tap only when Google actually demands one.

- List every profile on the account first, because one account can hold several profiles with near-identical names that differ only in capitalization or a trailing word.

- Identify the target profile by its service areas and its Business Profile ID, never by name alone.

- Read the Business Profile ID from the appeals tool listing or from the mpd value in the profile's own Edit URL, and quote that ID in any support case so the case lands on the right profile.

- Leave sibling profiles untouched unless the user explicitly orders work on them, and decline Google's offers to copy a post or edit across to a sibling profile.

## Audit before editing

- Read the live profile end to end and record phone, description, services, service areas, hours, attributes, photos, reviews, and posts with the date of the audit.

- Expect Google to mutate a profile on its own, including rewritten descriptions, changed service areas, junk services it invented, and a wrong opening date, and treat anything not re-read today as unverified.

- Compare the profile against the business website and flag every mismatch in name, number, areas, and hours before changing anything.

- Check the review count and average rating and write them down, because artwork and copy elsewhere often claim a rating the profile does not show.

## Fix the basics

- Submit phone and description edits knowing Google holds them in review, up to 7 days for those fields and about a day for services, and report them as pending rather than done until a later read shows them live.

- Write the description with the full business name, the real service footprint in words, and the true differentiators, and keep it free of claims the business cannot back.

- Prune services Google invented or that the business does not offer, add real missing services, and write a plain one-line description for each service that remains.

- Respect the 20 service-area cap, remove areas before adding at the cap because adds at the cap fail silently, and keep the list matched to where crews actually work and to the website's own area list.

- Keep a home-based business set up as a service-area business with no public street address, and never geotag its photos at the owner's home.

- Set the veteran-owned and other truthful attributes the profile offers, and check hours against the website so both tell the same story.

- Do not plan on seeding Questions and Answers, because Google removed that feature from profiles entirely, and carry common questions on the business website FAQ instead.

## Feed the profile photos

- Ask the owner for a steady supply of real job photos, targeting 8 to 12 new photos a month dripped in 2 to 3 a week, with a stockpile of 25 to 30 to start.

- Prefer real on-site photos of the crew, the truck, and finished work over stock images and promo graphics.

- Read any graphic before uploading it and reject artwork that carries a phone number, a wrong rating claim, or a stale offer.

## Post without getting shut off

- Never put a phone number, a URL, or an email address in a post's text or in its artwork, because Google's posts content policy bans all three and the violation can cost the whole posting feature.

- Carry the phone number only on the post's Call now button, which is the one place Google allows it.

- Name the business in full in every post, keep the topic seasonal and local to the real service areas, and rotate topics so no two posts repeat the same text.

- Check the Posts list after publishing and report the post as live only when it shows there, because a finished publish flow is not proof Google accepted the post.

- Remember that one rejected post is a warning and a second violation can turn posting off for the entire profile, so treat every draft as policy-checked before it goes up.

## Work the reviews

- Reply to new reviews from inside the profile and keep replies short, human, and free of arguments.

- Ask for reviews by text message right after a completed job, without gating unhappy customers away and without offering anything in exchange.

## Appeal a posting shutoff

- Treat the owner's email from Google as the authority on posting status, because the profile UI may show no banner, no notice, and a working Add update form while posting is in fact off.

- Delete the violating post first and confirm the deletion in the Posts list before filing anything.

- Hunt for the policy email in the owner's Gmail across All Mail, Spam, Trash, and the category tabs, searching the Routing ID and phrases like turned off posting and content policy.

- Check the owner's text messages for a screenshot of the email when the mailbox search comes up empty, because owners often forward the screenshot instead of the email itself.

- Expect the email to carry only Help Center and content policy links plus a Routing ID, with no appeal link, and do not wait for a magic link before acting.

- Check the Business Profile appeals tool, knowing it covers rejected content and may report no rejected content to appeal even when posting is off, and use it to confirm the exact Business Profile ID either way.

- File the case as an email support case started from inside the correct profile through its Help and support, Contact us path, and include the Routing ID and the Business Profile ID in the case body.

- Write the appeal plainly with what was deleted, what the violation was, the rule as you now understand it, and the process change that prevents a repeat, and ask for posting to be reinstated.

- Record the case ID the confirmation page shows, and tell the user the listing, reviews, rankings, and pending edits are unaffected while posting is off, with Google's reply expected over the following business days.

- Keep any scheduled posting job paused until Google reinstates posting and the user confirms the restart.

## Verify and log

- Re-read the profile after every Google review window and confirm each pending edit actually landed, because submitted is not the same as live.

- Log every profile action with its date, what changed, and its review state, so the next agent can see the history without re-asking the owner.

- Present results as exact values from the profile itself, including review counts, ratings, area lists, and case IDs, and label anything unconfirmed as unconfirmed.

## Instance notes (local overlay pattern)

- Instance notes for a specific business live in a never-published local overlay file kept outside this repo, referenced here by label only: the operator's business instance sheet. That overlay is never part of a published snapshot.
- Before working on a business's profiles, read that business's local instance sheet from the operator's private copy, and update it in place in that private copy whenever the live state changes.
- Generic guidance for any operator: keep one instance sheet per business in your own private overlay, recording the profile IDs, service areas, audit dates, pending edits, review counts, and case IDs for that business, and never publish that sheet with this skill.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Websites

- [Google Business Profile manager](https://business.google.com/locations) for profile edits, posts, photos, reviews, and the in-profile Help and support path. Carry the target profile's service areas and Business Profile ID into the browser task and verify them there before any change.

- [Google Business Profile Help](https://support.google.com/business) for the posts content policy and support flows. Read the policy from the page itself rather than from memory when a post or appeal is being drafted.

## Alternatives for better results

- Fix the website first when the profile and the site disagree, because Google and customers both read the site as the source of truth for name, number, and areas.

- Pair profile work with a Search Console check in the same session, confirming the sitemap reads clean and requesting indexing for the homepage and service areas pages after big site changes.
