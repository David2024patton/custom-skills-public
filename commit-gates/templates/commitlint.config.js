// Commit Gates: commit message gate configuration (commitlint).
//
// WHAT THIS IS: the shipped config for the commit message gate in
// commit-gates/SKILL.md. It extends config-conventional (Conventional
// Commits) with the repo standard's needs. Copy this file to the repo
// root as commitlint.config.js. It is wired into the commit-msg hook
// in both hook templates in this folder (.pre-commit-config.yaml and
// lefthook.yml) and re-checked in CI over the pull request commit
// range by the gates.yml template.
//
// REPO STANDARD EXTENSIONS over plain config-conventional:
//   - The type list below is the full atomic-commit vocabulary for
//     this standard: one commit carries one kind of change for one
//     module, and the type says which kind it is.
//   - The scope names the module the commit touches (the grid tile),
//     in lower case, matching the module names in docs and the module
//     map. A cross-module commit is a smell: split it instead.
//   - The body, when present, names the proof for the change and any
//     TODO item id or PLAN section it serves, so the message alone
//     ties the commit back to the repo standard's planning files.
//     That tie is a writing rule in docs/RULES.md; commitlint checks
//     the form it can check and the rest is review.
//   - Header and body lines stay at 100 characters so messages read
//     cleanly in plain git log output on any terminal.
//
// INSTALL (per repo, pinned in the repo lockfile where one exists):
//   npm install --save-dev @commitlint/cli @commitlint/config-conventional

module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'build',
        'chore',
        'ci',
        'docs',
        'feat',
        'fix',
        'perf',
        'refactor',
        'revert',
        'style',
        'test',
      ],
    ],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [
      2,
      'never',
      ['sentence-case', 'start-case', 'pascal-case', 'upper-case'],
    ],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100],
    'body-leading-blank': [1, 'always'],
    'body-max-line-length': [2, 'always', 100],
    'footer-leading-blank': [1, 'always'],
  },
};
