#!/usr/bin/env node
// === CRITIC SCRIPT MANIFEST ===
// question: Does the target's own sanitizer module stop the family XSS corpus when it is imported and executed directly?
// stackDetection: none (child process of sanitize-gate.mjs; the parent selects the module and the stack).
// inputs: argv MODULE_PATH REFENV_DIR MODE; env SANITIZE_GATE_CORPUS (corpus YAML path)
// effects: imports and executes the target module inside the review sandbox; read-only otherwise.
// exits: 0 always on a completed protocol run (the verdict travels in the JSON line); 3 on runner error before the protocol starts.
// output: one JSON line on stdout: {ran:true,total,failures:[{id,class,issues}]} or {ran:false,reason}
// === END MANIFEST ===
/*
 * target-module-runner.mjs - child process for sanitize-gate leg D.
 * Picks the sanitize function from the target module: a default export
 * that is a function, a named sanitize export, an object with a sanitize
 * method, or the DOMPurify instance shape (object with .sanitize).
 * The corpus is loaded through the same python3 plus PyYAML bridge the
 * parent gate uses, and outputs are judged with the same invariants,
 * parsed in the refenv jsdom so the judge does not depend on whatever
 * the target installed.
 * No em dashes are used anywhere in this tooling by family rule.
 */
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const [modulePath, refenv, mode] = process.argv.slice(2);
const corpusPath = process.env.SANITIZE_GATE_CORPUS;
const done = (obj) => { console.log(JSON.stringify(obj)); process.exit(0); };

let mod;
try {
  mod = await import(pathToFileURL(modulePath).href);
} catch (e) {
  done({ ran: false, reason: `import failed: ${String(e.message || e).slice(0, 240)}` });
}
const pick = (o) => {
  if (!o || (typeof o !== 'object' && typeof o !== 'function')) return null;
  if (typeof o === 'function') return o;
  if (typeof o.sanitize === 'function') return o.sanitize.bind(o);
  return null;
};
let fn = pick(mod) || pick(mod.default);
if (!fn) {
  for (const k of Object.keys(mod)) {
    if (/sanitize/i.test(k)) { fn = pick(mod[k]); if (fn) break; }
  }
}
if (!fn) done({ ran: false, reason: 'module imported but no sanitize function export was found (looked for a function default export, a sanitize export, or an object with a sanitize method)' });

const py = spawnSync('python3', ['-c',
    'import sys, json, yaml; d = yaml.safe_load(open(sys.argv[1])); print(json.dumps([{ "id": e["id"], "class": e["class"], "payload": e["payload"], "core": bool(e.get("core")), "hasExpected": e.get("expected_upstream") is not None } for e in d["entries"]]))',
  corpusPath], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
if (py.status !== 0) done({ ran: false, reason: `corpus load failed inside the runner: ${(py.stderr || '').trim().slice(0, 200)}` });
let entries = JSON.parse(py.stdout);
if (mode === 'quick') entries = entries.filter((e) => e.core);

let JSDOM;
try { ({ JSDOM } = createRequire(`${refenv}/package.json`)('jsdom')); }
catch (e) { done({ ran: false, reason: `refenv jsdom unavailable for output judging: ${e.message}` }); }
const { VirtualConsole } = createRequire(`${refenv}/package.json`)('jsdom');
const dom = new JSDOM('<!DOCTYPE html><body></body>', { virtualConsole: new VirtualConsole() });
const parse = (html) => { dom.window.document.body.innerHTML = html; return dom.window.document; };
const textOf = (html) => (parse(html).body.textContent || '').replace(/\s+/g, ' ').trim();
// Same invariants as sanitize-gate.mjs, kept in step by hand: attack
// issues for every class; benign preservation is a failure only where
// upstream recorded an expectation, otherwise a divergence note the
// parent surfaces in its own records. Legacy CSS javascript: tokens in
// style values are retained by the reference sanitizer on purpose and
// are not scored; expression() and -moz-binding are.
function attackIssues(output) {
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
      if (n === 'style' && /(expression\(|-moz-binding)/.test(v)) issues.push('css-attack');
    }
  });
  return [...new Set(issues)];
}
function check(entry, output) {
  if (entry.class !== 'benign-control') return attackIssues(output);
  const issues = attackIssues(output);
  const want = textOf(entry.payload);
  if (want && textOf(output) !== want && entry.hasExpected) {
    issues.push('benign-text-not-preserved');
    if (output.trim() === '') issues.push('benign-output-empty');
  }
  return [...new Set(issues)];
}

const failures = [];
for (const e of entries) {
  let issues;
  try { issues = check(e, String(fn(e.payload) ?? '')); }
  catch (err) { issues = [`sanitizer-threw:${String(err.message || err).slice(0, 120)}`]; }
  if (issues.length) failures.push({ id: e.id, class: e.class, issues });
}
done({ ran: true, total: entries.length, failures });
