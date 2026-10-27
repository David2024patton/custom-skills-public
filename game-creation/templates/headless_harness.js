#!/usr/bin/env node
/*
 * Headless harness: run UNMODIFIED legacy browser calculator/simulator JS in Node,
 * so recovered formulas can be executed and compared against a new engine.
 *
 * Copy, then edit BASE, FILES and the run() section.
 *   node harness.js
 *
 * Pattern: stub just enough DOM for the scripts to load, seed Math.random for
 * reproducibility, load files into one vm context in their original <script> order,
 * set form inputs via the stubbed elements, call the page's own compute function,
 * then read results from globals or element.innerHTML.
 */
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path');

const BASE = '/path/to/recovered/scripts';           // EDIT
const FILES = ['global.js', 'data.js', 'combat.js']; // EDIT: same order as the page's <script> tags

// Deterministic LCG so runs are repeatable (originals call Math.random()).
let seed = 0x20060101;
const rnd = () => ((seed = (1664525 * seed + 1013904223) >>> 0) / 0x100000000);
const math = Object.create(Math); math.random = rnd;

const el = Object.create(null);
const element = (v = '') => ({ value: String(v), checked: false, selectedIndex: 0, options: [], style: {}, innerHTML: '',
  appendChild() {}, removeChild() {}, setAttribute() {}, focus() {} });
const get = id => el[id] || (el[id] = element());
const document = {
  title: 'headless', forms: [], cookie: '',
  getElementById: get, getElementsByName: () => [], getElementsByTagName: () => [element()],
  createElement: () => element(), write() {}, writeln() {}
};
const windowStub = { alert: m => console.log('[alert]', m), open: () => {}, location: { href: '', search: '' } };
const ctx = { console, Math: math, document, window: windowStub, navigator: { userAgent: 'node' },
  alert: windowStub.alert, setTimeout: () => 0, clearTimeout() {}, parseInt, parseFloat, isNaN, escape, unescape };
ctx.self = ctx.window = Object.assign(windowStub, ctx);
vm.createContext(ctx);
for (const f of FILES) vm.runInContext(fs.readFileSync(path.join(BASE, f), 'utf8'), ctx, { filename: f });

// ---- run(): EDIT for the specific tool ------------------------------------
// Example: set inputs, call the page's compute function, collect N trials.
// get('attackerShip').value = 'Destroyer';
// const results = [];
// for (let i = 0; i < 1000; i++) { seed = 1000 + i; vm.runInContext('simulate()', ctx); results.push(get('output').innerHTML); }
// console.log(JSON.stringify(summary(results), null, 2));
console.log('Loaded globals:', Object.keys(ctx).filter(k => !['console','Math','document','window','self'].includes(k)).slice(0, 60).join(', '));
