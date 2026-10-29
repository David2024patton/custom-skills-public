#!/usr/bin/env node
// === CRITIC SCRIPT MANIFEST ===
// question: Does this web target sanitize user HTML with a current canonical sanitizer, on every sink, and does its sanitizer configuration actually stop the family XSS corpus?
// stackDetection: manifest stacks javascript, typescript, react, nextjs (the gate takes --stack for evidence labeling; the checks are the shared web sanitizer surface from references/languages/{javascript,typescript,react}.yaml).
// inputs: --root DIR (target), --stack NAME, --mode quick|full, --corpus PATH (default references/xss-payloads.yaml resolved from the critic bundle root), --refenv DIR (default scripts/sanitize/refenv next to this file), --out PATH (optional extra JSONL evidence file)
// effects: read-only on the target; the reference leg loads the pinned isomorphic-dompurify install in the refenv directory; the target-module leg imports a target sanitizer module in a child process (that executes target code, inside the review sandbox only).
// exits: 0 clean; 1 findings; 2 the corpus execution leg could not run (DID-NOT-RUN, stated in the summary); 3 gate error; 124 timeout (imposed by the caller).
// output: JSON lines on stdout (records: inventory, sink, corpus, target-module, summary); human summary on stderr.
// === END MANIFEST ===
/*
 * sanitize-gate.mjs - executable sanitizer gate for the Critic family.
 *
 * Legs:
 *   A inventory: sanitizer declarations in package.json files (dompurify,
 *     isomorphic-dompurify) with versions, resolved versions from
 *     package-lock.json where present, and stale-pin verdicts against the
 *     floor in references/languages/javascript.yaml (current known release
 *     3.4.17 at 2026-10-28; a pin is stale when it is more than one minor
 *     behind, per that file's currency_rule). happy-dom anywhere in the
 *     dependency set is a finding: the DOMPurify project names it unsafe
 *     and it is never an acceptable DOM host. Old jsdom is flagged for the
 *     same reason the language file gives. Config widenings found in
 *     source (ADD_TAGS, ADD_ATTR, addHook, USE_PROFILES) are findings.
 *   B sinks: source-level grep for the dangerous sinks listed in the
 *     javascript, typescript, and react language files. A sink is
 *     reported when no sanitize call is visible in its statement window.
 *     This leg is labeled source-level heuristic evidence: it cannot see
 *     through wrappers defined in other files, and it says so per record.
 *   C corpus execution: the family XSS corpus (references/
 *     xss-payloads.yaml) is executed through the pinned reference
 *     isomorphic-dompurify install and every output is checked against
 *     the entry invariant by parsing the output in jsdom. Quick mode
 *     runs core entries only; full mode runs all entries. The corpus is
 *     parsed through python3 with PyYAML, the family runtime; if that is
 *     unavailable this leg reports DID-NOT-RUN and the gate exits 2 when
 *     nothing else failed.
 *   D target module (full mode only): where the target itself ships an
 *     importable sanitizer module, the same corpus is executed through
 *     it in a child process, and the outcome or the concrete reason it
 *     could not run is recorded.
 *
 * No em dashes are used anywhere in this tooling by family rule.
 */
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync, appendFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const GATE_DIR = dirname(fileURLToPath(import.meta.url));
const args = {};
for (let i = 2; i < process.argv.length; i += 2) {
  const k = process.argv[i];
  if (!k || !k.startsWith('--')) { console.error(`bad argument: ${k}`); process.exit(3); }
  args[k.slice(2)] = process.argv[i + 1];
}
const ROOT = resolve(args.root || '.');
const STACK = args.stack || 'web';
const MODE = args.mode || 'full';
if (!['quick', 'full'].includes(MODE)) { console.error(`bad --mode: ${MODE}`); process.exit(3); }
const CORPUS = args.corpus ? resolve(args.corpus) : resolve(GATE_DIR, '../../references/xss-payloads.yaml');
const REFENV = args.refenv ? resolve(args.refenv) : join(GATE_DIR, 'refenv');
const OUT = args.out ? resolve(args.out) : null;
if (!existsSync(ROOT)) { console.error(`target root missing: ${ROOT}`); process.exit(3); }
if (OUT) writeFileSync(OUT, '');

const records = [];
function emit(rec) {
  records.push(rec);
  const line = JSON.stringify(rec);
  console.log(line);
  if (OUT) appendFileSync(OUT, line + '\n');
}
let findingCount = 0;
function finding(kind, severity, msg, extra = {}) {
  findingCount += 1;
  emit({ type: 'finding', kind, severity, stack: STACK, message: msg, ...extra });
}

// Sanitizer currency basis, stamped from references/languages/javascript.yaml
// (latest_known 3.4.17, verified 2026-10-28). Refresh at intel-refresh.
const KNOWN_CURRENT = { major: 3, minor: 4, patch: 17 };
const JSDOM_MIN_MAJOR = 24; // below the maintained line; old jsdom has documented XSS holes per DOMPurify

const SKIP_DIRS = new Set(['node_modules', '.git', 'dist', 'build', 'coverage', '.next', '.turbo', 'vendor']);
const TEST_PATH = /(^|\/)(test|tests|__tests__|__mocks__|fixtures?)\//;
function* walk(dir, depth, maxDepth) {
  if (depth > maxDepth) return;
  let ents;
  try { ents = readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const e of ents) {
    const p = join(dir, e.name);
    if (e.isDirectory()) {
      if (!SKIP_DIRS.has(e.name)) yield* walk(p, depth + 1, maxDepth);
    } else if (e.isFile()) yield p;
  }
}
const firstSemver = (spec) => {
  const m = /(\d+)\.(\d+)\.(\d+)/.exec(String(spec || ''));
  return m ? { major: +m[1], minor: +m[2], patch: +m[3], text: m[0] } : null;
};
const staleDomPurify = (v) => v && (v.major < KNOWN_CURRENT.major || (v.major === KNOWN_CURRENT.major && v.minor <= KNOWN_CURRENT.minor - 2));

// ---------------------------------------------------------------- Leg A
function legInventory() {
  const pkgFiles = [...walk(ROOT, 0, 4)].filter((p) => p.endsWith('package.json'));
  let declared = 0;
  let sanitizerSeen = false;
  const lockVersions = {};
  for (const lf of [...walk(ROOT, 0, 2)].filter((p) => p.endsWith('package-lock.json'))) {
    try {
      const lock = JSON.parse(readFileSync(lf, 'utf8'));
      for (const [path, info] of Object.entries(lock.packages || {})) {
        const name = path.replace(/^node_modules\//, '');
        if (['dompurify', 'isomorphic-dompurify', 'jsdom', 'happy-dom'].includes(name) && info.version) lockVersions[name] = info.version;
      }
    } catch { /* unreadable lockfile: inventory proceeds on declarations */ }
  }
  for (const pf of pkgFiles) {
    let pkg;
    try { pkg = JSON.parse(readFileSync(pf, 'utf8')); } catch { continue; }
    const deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}), ...(pkg.peerDependencies || {}) };
    const rel = relative(ROOT, pf);
    for (const name of ['dompurify', 'isomorphic-dompurify', 'jsdom', 'happy-dom']) {
      if (!(name in deps)) continue;
      declared += 1;
      const spec = deps[name];
      const resolved = lockVersions[name] || null;
      const eff = firstSemver(resolved) || firstSemver(spec);
      const rec = { type: 'inventory', package: name, declaredSpec: spec, resolvedVersion: resolved, effectiveVersion: eff ? eff.text : null, file: rel, stack: STACK };
      emit(rec);
      if (name === 'dompurify') {
        sanitizerSeen = true;
        if (eff && staleDomPurify(eff)) finding('stale-sanitizer-pin', 'high',
          `dompurify pinned at ${eff.text}; the floor from references/languages/javascript.yaml flags pins more than one minor behind the current known release ${KNOWN_CURRENT.major}.${KNOWN_CURRENT.minor}.${KNOWN_CURRENT.patch}`,
          { file: rel, package: name, version: eff.text });
        else if (!eff) emit({ type: 'note', kind: 'unpinned-spec', package: name, file: rel, message: `dompurify spec "${spec}" carries no resolvable version; currency could not be verified from declarations` });
      }
      if (name === 'isomorphic-dompurify') {
        sanitizerSeen = true;
        if (eff && eff.major < 2) finding('stale-sanitizer-pin', 'high',
          `isomorphic-dompurify pinned at ${eff.text}; the 1.x line wraps the DOMPurify 2 series, behind the floor in references/languages/javascript.yaml`,
          { file: rel, package: name, version: eff.text });
      }
      if (name === 'happy-dom') finding('unsafe-dom-host', 'high',
        'happy-dom is declared; the DOMPurify project names happy-dom unsafe as a DOM host for sanitization and it is never an acceptable substitute',
        { file: rel, package: name });
      if (name === 'jsdom' && eff && eff.major < JSDOM_MIN_MAJOR) finding('stale-dom-host', 'medium',
        `jsdom pinned at ${eff.text}; DOMPurify documentation warns that old jsdom versions contain XSS holes even when DOMPurify itself is perfect`,
        { file: rel, package: name, version: eff.text });
    }
  }
  // Config widenings in sources that touch DOMPurify.
  const widenRe = /\b(ADD_TAGS|ADD_ATTR|addHook|USE_PROFILES)\b/;
  for (const f of [...walk(ROOT, 0, 6)].filter((p) => /\.(mjs|cjs|js|jsx|ts|tsx)$/.test(p) && !TEST_PATH.test(relative(ROOT, p)))) {
    let text;
    try { text = readFileSync(f, 'utf8'); } catch { continue; }
    if (!/dompurify/i.test(text)) continue;
    text.split('\n').forEach((line, i) => {
      if (widenRe.test(line)) finding('config-widening', 'medium',
        `sanitizer widening call requires review per references/languages/javascript.yaml config_checks: ${line.trim().slice(0, 160)}`,
        { file: relative(ROOT, f), line: i + 1, evidence: 'source-level' });
    });
  }
  return { declared, sanitizerSeen };
}

// ---------------------------------------------------------------- Leg B
const SINKS = [
  { kind: 'innerHTML', re: /\.innerHTML\s*\+?=/, label: 'innerHTML assignment (javascript.yaml dangerous_sinks)' },
  { kind: 'outerHTML', re: /\.outerHTML\s*\+?=/, label: 'outerHTML assignment (javascript.yaml dangerous_sinks)' },
  { kind: 'insertAdjacentHTML', re: /\.insertAdjacentHTML\s*\(/, label: 'insertAdjacentHTML (javascript.yaml dangerous_sinks)' },
  { kind: 'document-write', re: /document\.write(?:ln)?\s*\(/, label: 'document.write (javascript.yaml dangerous_sinks)' },
  { kind: 'jquery-html', re: /\.html\s*\(\s*[A-Za-z_$]/, label: 'jQuery .html() with a non-literal argument (javascript.yaml dangerous_sinks)' },
  { kind: 'href-src-assignment', re: /\.(href|src)\s*=\s*[A-Za-z_$]/, label: 'href or src assigned a variable without visible scheme validation (javascript and react language files)' },
  { kind: 'setattribute-url', re: /setAttribute\s*\(\s*['"](href|src)['"]\s*,\s*[A-Za-z_$]/, label: 'setAttribute href or src with a variable (javascript and react language files)' },
  { kind: 'dangerouslySetInnerHTML', re: /dangerouslySetInnerHTML/, label: 'dangerouslySetInnerHTML (react.yaml dangerous_sinks)' },
  { kind: 'ts-double-assertion', re: /as\s+unknown\s+as\s+string/, label: 'double assertion pushing data past a typed sanitizer boundary (typescript.yaml dangerous_sinks)' },
];
function legSinks() {
  let filesScanned = 0, sinksFound = 0, filesSkippedTest = 0;
  const files = [...walk(ROOT, 0, 8)].filter((p) => /\.(mjs|cjs|js|jsx|ts|tsx|vue|svelte)$/.test(p) && !p.endsWith('.min.js'));
  for (const f of files) {
    const rel = relative(ROOT, f);
    if (TEST_PATH.test(rel) || /\.(test|spec)\./.test(rel)) { filesSkippedTest += 1; continue; }
    let text;
    try { if (statSync(f).size > 1_000_000) continue; text = readFileSync(f, 'utf8'); } catch { continue; }
    filesScanned += 1;
    const lines = text.split('\n');
    lines.forEach((line, i) => {
      for (const sink of SINKS) {
        const m = sink.re.exec(line);
        if (!m) continue;
        sinksFound += 1;
        // Statement window: the sink line plus the two following lines,
        // which covers the common multi-line assignment shapes.
        const window = lines.slice(i, i + 3).join('\n');
        const sinkIdx = window.indexOf(m[0]);
        const before = window.slice(0, sinkIdx);
        const clean = /sanitize\s*\(/.test(window) && (/sanitize\s*\(/.test(before) || /=\s*[^;]*sanitize\s*\(/.test(window) || /__html\s*:\s*[^,}]*sanitize\s*\(/.test(window) || /\(\s*sanitize\s*\(/.test(window));
        emit({ type: 'sink', kind: sink.kind, file: rel, line: i + 1, sanitizedInline: clean, evidence: 'source-level', stack: STACK, text: line.trim().slice(0, 200) });
        if (!clean) finding('unsanitized-sink', 'high',
          `${sink.label}: no sanitize call visible in the sink statement window. Source-level heuristic evidence; a wrapper in another file cannot be seen by this leg and the verdict says so.`,
          { file: rel, line: i + 1, sink: sink.kind, evidence: 'source-level' });
      }
    });
  }
  return { filesScanned, sinksFound, filesSkippedTest };
}

// ---------------------------------------------------------------- Corpus
function loadCorpus() {
  const py = spawnSync('python3', ['-c',
    'import sys, json, yaml; d = yaml.safe_load(open(sys.argv[1])); print(json.dumps([{ "id": e["id"], "class": e["class"], "payload": e["payload"], "core": bool(e.get("core")), "hasExpected": e.get("expected_upstream") is not None } for e in d["entries"]]))',
    CORPUS], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (py.status !== 0) return { error: `corpus load failed: ${(py.stderr || '').trim().slice(0, 300)}` };
  try { return { entries: JSON.parse(py.stdout) }; } catch (e) { return { error: `corpus parse failed: ${e.message}` }; }
}

function invariantChecker(JSDOM) {
  // The JSDOM instances in this gate run with a swallowed virtual
  // console: payload CSS that jsdom cannot parse is evidence about the
  // payload, not gate noise on stderr.
  const { VirtualConsole } = createRequire(join(REFENV, 'package.json'))('jsdom');
  const vc = new VirtualConsole();
  const dom = new JSDOM('<!DOCTYPE html><body></body>', { virtualConsole: vc });
  const { window } = dom;
  const parse = (html) => { window.document.body.innerHTML = html; return window.document; };
  const textOf = (html) => (parse(html).body.textContent || '').replace(/\s+/g, ' ').trim();
  const attackIssues = (output) => {
    const issues = [];
    if (/<script[\s>/]/i.test(output)) issues.push('script-markup-in-output');
    const doc = parse(output);
    doc.querySelectorAll('script').forEach(() => issues.push('script-element-survives'));
    doc.querySelectorAll('*').forEach((el) => {
      for (const attr of el.attributes || []) {
        const n = attr.name.toLowerCase();
        const v = (attr.value || '').replace(/[\s\u0000-\u0020]+/g, '').toLowerCase();
        if (n.startsWith('on')) issues.push(`event-handler-attr:${n}`);
        if (['href', 'src', 'action', 'formaction', 'xlink:href'].includes(n) && /^(javascript:|vbscript:|data:text\/html|view-source:)/.test(v)) issues.push(`dangerous-url:${n}`);
        if (n === 'srcdoc') issues.push('srcdoc-attr');
        // Executable CSS primitives only. A javascript: token inside a
        // style value is a legacy vector (old Opera and IE CSS) that the
        // reference sanitizer deliberately retains; its own test suite
        // expects retention, and no current browser executes it. The
        // gate follows the reference security model here and says so.
        if (n === 'style' && /(expression\(|-moz-binding)/.test(v)) issues.push('css-attack');
      }
    });
    return [...new Set(issues)];
  };
  return function check(entry, output) {
    if (entry.class === 'benign-control') {
      const issues = attackIssues(output);
      const notes = [];
      const want = textOf(entry.payload);
      const got = textOf(output);
      if (want && got !== want) {
        // Preservation is a finding only where upstream recorded an
        // expectation (the content is meant to survive). Inline suite
        // snippets without an upstream expectation are config probes;
        // their divergence is recorded as a note, not a defect.
        if (entry.hasExpected) { issues.push('benign-text-not-preserved'); if (output.trim() === '') issues.push('benign-output-empty'); }
        else notes.push('benign-divergence-no-upstream-expectation');
      }
      return { issues: [...new Set(issues)], notes };
    }
    return { issues: attackIssues(output), notes: [] };
  };
}

function runCorpusThrough(sanitizeFn, entries, check, legName) {
  let failed = 0;
  for (const e of entries) {
    let out, verdict;
    try { out = sanitizeFn(e.payload); verdict = check(e, String(out ?? '')); }
    catch (err) { verdict = { issues: [`sanitizer-threw:${String(err.message || err).slice(0, 120)}`], notes: [] }; }
    const { issues, notes } = verdict;
    const pass = issues.length === 0;
    if (!pass) failed += 1;
    emit({ type: 'corpus', leg: legName, id: e.id, class: e.class, result: pass ? 'pass' : 'fail', issues, notes, stack: STACK });
    if (!pass) finding('corpus-failure', 'high', `corpus entry ${e.id} (${e.class}) survives sanitization: ${issues.join(', ')}`, { leg: legName, corpusId: e.id, class: e.class });
  }
  return { total: entries.length, failed };
}

// ---------------------------------------------------------------- Leg C
function legReference(entries) {
  const dpPath = join(REFENV, 'node_modules', 'isomorphic-dompurify');
  if (!existsSync(dpPath)) {
    emit({ type: 'did-not-run', leg: 'reference-corpus', reason: `reference install missing at ${dpPath}; npm install in scripts/sanitize/refenv restores it`, stack: STACK });
    return { ran: false };
  }
  let DOMPurify, JSDOM;
  try {
    const req = createRequire(join(REFENV, 'package.json'));
    DOMPurify = req('isomorphic-dompurify');
    ({ JSDOM } = req('jsdom'));
  } catch (e) {
    emit({ type: 'did-not-run', leg: 'reference-corpus', reason: `reference install failed to load: ${e.message}`, stack: STACK });
    return { ran: false };
  }
  const dpVersion = (() => { try { return JSON.parse(readFileSync(join(REFENV, 'node_modules', 'dompurify', 'package.json'), 'utf8')).version; } catch { return 'unknown'; } })();
  emit({ type: 'note', kind: 'reference-sanitizer', message: `reference leg runs isomorphic-dompurify over jsdom with dompurify ${dpVersion} (refenv pinned install)`, stack: STACK });
  const check = invariantChecker(JSDOM);
  const res = runCorpusThrough((h) => DOMPurify.sanitize(h), entries, check, 'reference-corpus');
  return { ran: true, ...res };
}

// ---------------------------------------------------------------- Leg D
function legTargetModule(entries) {
  const candidates = [];
  for (const f of [...walk(ROOT, 0, 6)]) {
    const rel = relative(ROOT, f);
    if (TEST_PATH.test(rel)) continue;
    if (/(^|\/)(sanitize|sanitizer|purify|xss)[^/]*\.(mjs|cjs|js)$/i.test(rel)) { candidates.push(f); continue; }
    if (/\.(mjs|cjs|js)$/.test(rel)) {
      try {
        const t = readFileSync(f, 'utf8');
        if (/export\s+(async\s+)?(function|const|let|var)\s+\w*[Ss]anitize|exports\.\w*[Ss]anitize\s*=|module\.exports\s*=.*[Ss]anitize/s.test(t) && /dompurify/i.test(t)) candidates.push(f);
      } catch { /* unreadable file: not a candidate */ }
    }
  }
  if (!candidates.length) {
    const tsOnly = [...walk(ROOT, 0, 6)].some((p) => /(sanitize|sanitizer|purify)/i.test(relative(ROOT, p)) && /\.tsx?$/.test(p));
    emit({ type: 'did-not-run', leg: 'target-module', reason: tsOnly ? 'target sanitizer module is TypeScript; it requires a build step and was not executed' : 'no importable sanitizer module found in the target', stack: STACK });
    return { ran: false, reason: 'no-candidate' };
  }
  if (!existsSync(join(ROOT, 'node_modules'))) {
    emit({ type: 'did-not-run', leg: 'target-module', reason: 'target dependencies not installed (node_modules absent at target root); the module could not be imported', candidate: relative(ROOT, candidates[0]), stack: STACK });
    return { ran: false, reason: 'deps-not-installed' };
  }
  const child = join(GATE_DIR, 'target-module-runner.mjs');
  const r = spawnSync('node', [child, candidates[0], REFENV, MODE], {
    cwd: ROOT, encoding: 'utf8', timeout: 180_000, maxBuffer: 64 * 1024 * 1024,
    env: { ...process.env, SANITIZE_GATE_CORPUS: CORPUS },
  });
  if (r.status !== 0 || !r.stdout) {
    emit({ type: 'did-not-run', leg: 'target-module', reason: `target module run failed: ${(r.stderr || r.error?.message || 'no output').trim().slice(0, 300)}`, candidate: relative(ROOT, candidates[0]), stack: STACK });
    return { ran: false, reason: 'child-failed' };
  }
  let res;
  try { res = JSON.parse(r.stdout.trim().split('\n').pop()); } catch {
    emit({ type: 'did-not-run', leg: 'target-module', reason: 'target module runner returned unparseable output', candidate: relative(ROOT, candidates[0]), stack: STACK });
    return { ran: false, reason: 'child-output' };
  }
  if (!res.ran) {
    emit({ type: 'did-not-run', leg: 'target-module', reason: res.reason, candidate: relative(ROOT, candidates[0]), stack: STACK });
    return { ran: false, reason: res.reason };
  }
  for (const f of res.failures) {
    emit({ type: 'corpus', leg: 'target-module', id: f.id, class: f.class, result: 'fail', issues: f.issues, stack: STACK });
    finding('corpus-failure', 'high', `corpus entry ${f.id} (${f.class}) survives the TARGET sanitizer module: ${f.issues.join(', ')}`, { leg: 'target-module', corpusId: f.id, class: f.class });
  }
  emit({ type: 'note', kind: 'target-module-result', message: `target sanitizer module ${relative(ROOT, candidates[0])} executed over ${res.total} corpus entries, ${res.failures.length} failures`, stack: STACK });
  return { ran: true, total: res.total, failed: res.failures.length };
}

// ---------------------------------------------------------------- Main
const started = Date.now();
const inv = legInventory();
const sinks = legSinks();
let execOk = false;
let corpusInfo = { ran: false };
let targetInfo = { ran: false };
const corpus = loadCorpus();
if (corpus.error) {
  emit({ type: 'did-not-run', leg: 'reference-corpus', reason: corpus.error, stack: STACK });
} else {
  const entries = MODE === 'quick' ? corpus.entries.filter((e) => e.core) : corpus.entries;
  corpusInfo = legReference(entries);
  execOk = !!corpusInfo.ran;
  if (MODE === 'full' && execOk) targetInfo = legTargetModule(entries);
  else if (MODE === 'full') targetInfo = { ran: false, reason: 'reference leg did not run' };
}
const exit = findingCount > 0 ? 1 : (execOk ? 0 : 2);
emit({
  type: 'summary', stack: STACK, mode: MODE, root: ROOT,
  sanitizerDeclared: inv.sanitizerSeen, sinkFilesScanned: sinks.filesScanned,
  sinkFilesSkippedAsTests: sinks.filesSkippedTest, sinksFound: sinks.sinksFound,
  corpus: corpusInfo, targetModule: targetInfo,
  findings: findingCount, exit, durationMs: Date.now() - started,
});
console.error(`sanitize-gate: stack=${STACK} mode=${MODE} findings=${findingCount} sinks=${sinks.sinksFound} corpus=${corpusInfo.ran ? `${corpusInfo.total - corpusInfo.failed}/${corpusInfo.total} passed` : 'DID-NOT-RUN'} target-module=${targetInfo.ran ? `${targetInfo.total - targetInfo.failed}/${targetInfo.total} passed` : 'did-not-run'} exit=${exit}`);
process.exit(exit);
