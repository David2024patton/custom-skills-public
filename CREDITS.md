# Credits

This library builds on open work by other people. This file names
them and what this repo takes from each. Both works below are MIT
licensed; the upstream license texts travel with the vendored files
named here, and each vendored unit carries its own PROVENANCE.md
with the exact source commit.

## morluto: REA

Upstream: https://github.com/morluto/rea (MIT, Copyright (c) 2026
morluto). REA, "Reverse engineer anything with agents," is taken
four ways:

- The engine itself, wrapped and never embedded, by the
  `rea-engine` unit (skills/software-development/rea-engine):
  server `rea-agents` 6.8.0 with skill bundle version 50, called
  as a pinned external process.
- Two of its prose skills, vendored whole as library units:
  `rea-ci-tests-audit` and `rea-tool-design`
  (skills/software-development/).
- Its instructions-only skill bundle, vendored as reference text
  inside the `rea-engine` unit.
- Its reverse engineering methods, harvested for the Critic in the
  2026-10-27 dissection (change specs CS-01 to CS-18: behavior
  inventory with a two-directional claims diff, runtime
  observation, evidence workflows, the CI and tests audit,
  perturbation probes, mutation calibration, scoped zero, and the
  rest).

## Alex Netto (alextnetto): res

Upstream: https://github.com/alextnetto/res (MIT, Copyright (c)
2026 Alex Netto). res, the agent skill that reverse engineers a
SaaS product through the browser into a rebuild knowledge base, is
taken two ways:

- The skill itself, vendored whole as a library unit:
  `reverse-engineering-saas` (skills/research/), upstream files
  intact at v0.4.0.
- Its parity and check methods (parity maps, barrier analysis,
  knowledge-base checking), which feed the Critic's claims work
  through the same dissection's change specs.
