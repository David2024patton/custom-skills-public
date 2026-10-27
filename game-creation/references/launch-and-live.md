# Launch and live operations

Shipping is the midpoint. This chapter covers finding players, releasing cleanly, and running the game afterward.

## Market validation

- Before building past the prototype, write the one-sentence pitch, list 5 to 10 comparable titles with their reception and pricing, and name the gap this game fills. No gap, no build.

## Store page and marketing beats

- Stand up the store page at vertical slice: capsule art that reads at thumbnail size, a trailer that opens on real gameplay, honest tags, and screenshots of real play. Track wishlist velocity like a build metric.

- Put marketing beats in the same milestone list as dev stages: announcement, community home, demo, festival entry, and a launch window chosen against competing releases.

- Open the community channel at announcement and recruit playtesters from it, and gate creator builds behind the same playtest benchmarks as public demos.

## Compliance and release operations

- Keep a per-platform compliance checklist from pre-production: age ratings (start early, they gate the date), privacy policy and data-safety labels, required platform features, review timelines, and console certification where it applies, scheduled as a milestone with buffer for a failed first pass.

- Decide the money model in the concept stage (premium, free with cosmetic sales, ads, none), write its fairness rules next to the economy design, keep monetization out of the core loop's critical path, price transparently in real-money terms, and ban dark patterns such as obscured premium currency value, pay-to-skip timers, and manufactured urgency. Treat loot boxes and gambling-adjacent mechanics as regulated and region-dependent.

## Telemetry

- Define the event schema and key funnels during production (onboarding completion, retention, economy flows, difficulty deaths, stuck points), instrument them behind the same config system as tuning, respect consent and privacy rules, and verify in QA that the events actually fire.

## Live operations

- Spec the live-ops layer with the game: patch cadence, event calendar, remote configuration and feature flags so changes land without a client update where possible, and a rollback plan for when a change lands badly.

- For online games, spec the operations layer with the rules: account and save storage, backup cadence, matchmaking around skill and ping, server hosting and per-player cost, and community operations as a system (code of conduct, reporting and moderation tooling, ban appeals, mute and block defaults, no open voice by default).

- Review metrics weekly with a named decision maker, and communicate roadmaps and changes to players plainly.

## End of life

- Write the end-of-life plan while the game is healthy: how players are told, what happens to servers and saves, and an export of player data if the game ever closes. A revived game owes its players a better ending than the original got.
