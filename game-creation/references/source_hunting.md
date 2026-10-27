# Source Hunting and Evidence Discipline

## Where game knowledge survives (check all, in roughly this order)

| Source | What it gives | How to find |
|---|---|---|
| Official help or manual pages | Rules, equations, item tables, changelogs per version | CDX on the game domain, filtered for `help|topic=|manual|faq|changes|rules` |
| Official front and news pages, sampled yearly | Version and round timeline, launch and closure dates, successor announcements | CDX on the root URL without `collapse`; pick about 2 captures per year |
| **Fan calculators and simulators** | **Executable formulas** (combat, ship building, visibility, ports), with full stat tables | User leads, links from the official forums or wiki, CDX on fan domains filtered for `\.js$` |
| Fan wikis | Mechanics explanations, lore, item lists, screenshots | CDX for wiki domains; MediaWiki `index.php?title=` pages |
| Official downloadable packs (skins, images, `files/`) | Exact original graphics and CSS for pixel-faithful UI | CDX filtered for `\.(zip|rar|7z|tar|gz)$`; unpack with `unar` |
| Saved live pages or mirrors, trainer pages (for example getChief) | Real layout HTML, link and token formats, client timers | User links; `wget -p -k` on live mirrors |
| Forks and GPL relatives (for example Solar Empire, Blacknova) | Real server code for sister mechanics | GitHub, SourceForge, Google Code archives, `git clone` |
| Successor or sequel sites and dev blogs | Designer intent, what changed, why it failed | CDX on the successor domain, plus blog domains such as wordpress.com subdomains |
| Videos (YouTube battle recordings) | Pacing, timing, UI flow | `manus-analyze-video` with a specific question |

## Wayback mechanics

- **Raw mode:** use `https://web.archive.org/web/<ts>id_/<url>`. The `id_` suffix returns the original bytes with no toolbar and no rewritten links. Use it for anything you will parse or execute.
- **CDX:** `cdx/search/cdx?url=<domain>/*&output=txt&fl=timestamp,original,mimetype,length,statuscode&filter=statuscode:200&collapse=urlkey`. It's slow, so allow up to 240 s and retry with backoff. Query `www.` and bare domains separately, and old ports such as `:80`.
- **Filter before fetching.** Domains often host unrelated material (phpBB styles, other games, IRC applets). Exclude those, cap the size, and review the extension summary first. One unfiltered bulk fetch in the TDZK project stalled on large unrelated files.
- **Placeholder detection:** Wayback sometimes returns its own HTML (redirect notices, exclusions). `wayback_fetch.py` drops those pages and logs them.
- **Assets referenced by JS:** grep downloaded JS and HTML for `src=`, `.js`, and `files/`, then add any newly found URLs to a second round of fetching.

## Evidence tiers (label every claim)

1. **Official live or production evidence:** an official help page, changelog, front-page announcement or server code.
2. **Official artifacts:** image packs, downloadable files.
3. **Fan tools:** a calculator or simulator **labeled** with a version. That proves a tool existed for the label, **not** that it matched the live server.
4. **Community memory:** forum posts, wiki pages, the user's recollection.

Rules:
- Never merge versions silently. Keep data per version and record conflicts. In TDZK, the fan 2.8 simulator contradicted the official 2.7 changelog.
- Verify remembered numbers against the archive, and say plainly when memory differs from the evidence. Examples from TDZK: the user remembered "3.8", but 3.1 was the last live version; the user remembered "10 ships into combat", but the rule was "command ship plus 5".
- Mark pages that are self-labeled "OUTDATED" and prefer later changelogs over them.
- Cite capture timestamps and URLs in every reference document.

## Version timeline method

1. Run CDX on all official hosts, including MIME types other than HTML.
2. Grep the CDX for version-like tokens: `topic=.*Changes`, `v\d-\d`, `\d\.\d`, `hof/\d\.\d`.
3. Sample the front page at least once a year, and every launch and closure notice.
4. Build a table with these columns: version or round, dates, key changes, and an evidence citation.
5. Build a data-coverage matrix for each version, covering help, stats tables, combat code, calculators, station or map lists and image packs, with local paths and the gaps.
6. Recommend a target ruleset: the best-documented version, not necessarily the last one.
