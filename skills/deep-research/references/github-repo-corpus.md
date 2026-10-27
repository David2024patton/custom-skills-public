# Bulk GitHub repo ingestion and corpus mining

When David pastes a batch of GitHub links ("check these out", "maybe useful",
"do not skim, they must all be ingested"), the contract is FULL ingestion of
every repo, then a verdict per repo judged against his stack. Partial reads or
headline summaries of the listicle name are a miss.

## 1. Ingest the batch

- gitingest may not be installed: `"/c/Program Files/Python311/python.exe" -m
 pip install gitingest` (the Hermes venv python has no pip module on this
 host; py311 does).
- Loop over all URLs in one background script: `python -m gitingest <url>
 -o <out>/owner__repo.txt`, per-repo timeout ~300s, skip files already >3KB
 so a re-run resumes instead of restarting.
- Fallback per failed repo: curl the raw README (branches main then master,
 names README.md/readme.md/Readme.md) and write it with a header noting it
 is the README fallback. Never leave a repo silently missing from the batch;
 report the FAILED list explicitly.
- Output dir: `<workspace>/research/repos/` (name digests `owner__repo.txt`).

## 2. De-noise before anyone reads (monorepo digests explode)

A single monorepo digest can land at tens of MB because gitingest includes
eval results, run artifacts, bundled assets. De-noise before fan-out:

- The digest is sections: a run of `=` then `FILE: ` then the path on the
 NEXT line, then content. Parse the path as the line after the `FILE: `
 marker. Pitfall: re-prepending the separator to a split part mangles the
 name so every filter silently matches nothing while the file still shrinks
 (size-only filtering) and names read back as `======`. Print the first 10
 parsed names before filtering; if they are not paths, stop and fix the parse.
- Filter by path pattern: eval/results/, final_runs/, node_modules/,
 *.min.js, /dist/, /build/, *.log, raw JSON run outputs; drop sections
 >150KB. Keep methodology (suite definitions, skill profiles, prompts, docs)
 even under an evals/ tree - the harness design is the value, the per-run
 artifacts are noise.
- Verify after: count sections kept, size, and that skill/doc files survived.

## 3. Full-read fan-out (verdicts, no skimming)

Group digests into child briefs of roughly 250-500KB each; give a single
oversized digest its own child with instructions to read in chunks. Each
brief:

- Names its files and byte sizes and orders chunked reads via read_file.
- Requires INCREMENTAL notes written to a per-group notes file as it reads
 (the notes survive the child's context; the final JSON alone does not
 prove coverage).
- Carries the stack to judge against: AlphaFlux (Go multi-tenant SaaS),
 AlphaVision (TV OS), the retro game system (TDZK revival / iTaK Gaming),
 Patriot Pest Control, iTaK Learn, the the harness SDLC harness, the Hermes
 persona/critic pipeline, custom-skills repo.
- Per repo returns: what it is (evidence-based), reusable assets (condensed
 with actual content), VERDICT useful/not + why, WHERE IT FITS (one
 primary home), and concrete extraction actions (exact text to lift and its
 destination), plus `full_read_confirmed`.
- Account-for-bulk rule: every section either read or explicitly accounted
 as uniform bulk with counts. "I read the first part" fails the contract.

## 4. Synthesis

Merge children's verdicts into one mine-report: grouped by destination
(pipeline, AlphaFlux, AlphaVision, gaming, security, not-useful), with the
concrete wirings first. Verdicts against the stack, not generic summaries -
a repo is only "useful" when a named home and an extraction action exist.
