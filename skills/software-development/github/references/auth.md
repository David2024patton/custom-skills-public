# GitHub Authentication Setup

This file is the one place this skill states its authentication rule. Every
other reference in this skill points here instead of repeating its own setup.

## The rule

Agents authenticate only through `gh auth`. A GitHub token never enters agent
context, stdout, environment variables, a file the agent writes, or a chat
transcript. The agent never reads, extracts, copies, or prints a token, from
any credential file, keychain, or config. If `gh` is unavailable or not
logged in, stop and tell the user to install `gh` and run `gh auth login`.
There is no curl fallback, no token extraction fallback, and no git-only
fallback in this skill.

## Detection

Run this check first, once per session:

```bash
gh --version 2>/dev/null || echo "gh not installed"
gh auth status 2>/dev/null || echo "gh not authenticated"
```

Decision tree:

1. `gh auth status` shows authenticated: you are good, use `gh` for everything.
2. `gh` is installed but not authenticated: the user runs `gh auth login`
   (below), then you retry.
3. `gh` is not installed: stop. Tell the user to install it from
   https://cli.github.com and run `gh auth login`. Do not work around the
   missing login with tokens, credential files, or raw curl calls.

## Recommended path: gh auth login (the only recommended path)

The user runs this in their own terminal, so the credential flow stays
between the user, their browser, and `gh`:

```bash
gh auth login
# Select: GitHub.com
# Select: HTTPS
# Authenticate via browser (or the device code flow gh offers)
```

`gh` stores the credential in the operating system keychain where one is
available, or in its own protected config. Then wire git to use the same
login, and verify:

```bash
gh auth setup-git
gh auth status
```

Notes for agent driven sessions:

- If a browser cannot open from the session, `gh auth login` offers a
  one time device code the user enters at github.com/login/device. The code
  is shown to the user, who completes the flow themselves. Never ask the
  user to paste a token into the chat instead.
- On a headless machine where `gh auth login` cannot complete, the user
  runs the same command in their own SSH session on that machine. The agent
  still does not handle the credential.

## SSH keys (for git transport, optional)

If the user prefers SSH remotes, a key is fine, with a passphrase:

```bash
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"

# Generate only if needed. No -N flag: ssh-keygen prompts for a passphrase.
# A passphrase free key is not acceptable; if the prompt cannot be answered
# interactively, stop and let the user generate the key themselves.
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

The user adds the public key at https://github.com/settings/keys, then:

```bash
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."
```

## Git identity

Required for commits, and unrelated to authentication:

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

## Helper: detect auth state

`scripts/gh-env.sh` in this skill reports whether `gh` is authenticated and
which repo the current directory belongs to. Paths in this skill are
relative to the skill folder, where `scripts/` and `references/` are
siblings of `SKILL.md`:

```bash
source scripts/gh-env.sh
# Sets GH_AUTH_METHOD ("gh" or "none"), GH_USER, GH_OWNER, GH_REPO,
# GH_OWNER_REPO. It reads no credential files and sets no token variable.
```

Inline equivalent:

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "AUTH_METHOD=gh"
else
  echo "AUTH_METHOD=none"
  echo "Stop: ask the user to install gh and run 'gh auth login'."
fi
```

## Fine grained tokens (human operators only, never the agent)

Some server setups cannot use interactive `gh auth login`. A human operator
setting up such a machine may create a **fine grained** personal access
token, under these conditions only:

- Fine grained token, never a classic token. A classic token with broad
  scopes such as full `repo` plus `workflow` is not acceptable.
- Repository access limited to the named repositories the setup needs.
- Minimal permissions only, named one by one (for typical agent work:
  Contents read and write, Pull requests read and write, Issues read and
  write, Actions read). Nothing else.
- An expiry date is required. No non expiring tokens.
- The operator enters the token themselves, directly into `gh` storage
  (`gh auth login --with-token` in their own terminal) or the operating
  system keychain. The agent never sees, handles, or confirms the value.

Warning, plainly: a token is a password for the account. Never paste one
into a chat, a file, a script, or an issue. Never embed one in a remote URL,
where it persists in `.git/config` and leaks through `git remote -v`,
backups, and screen shares. Never store one in plaintext; configurations
that write tokens to a plain file on disk, including the git `store`
credential helper, are prohibited by this skill, not recommended by it.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `gh: command not found` | Stop. The user installs `gh` from https://cli.github.com and runs `gh auth login`. There is no fallback in this skill. |
| `gh auth status` says not logged in | The user runs `gh auth login` in their own terminal, then you retry. |
| `git push` asks for a password | Password auth is disabled by GitHub. Run `gh auth setup-git` so git uses the `gh` login. |
| `remote: Permission to X denied` | The `gh` login lacks access to that repo or org. The user checks org membership and SSO authorization on their account; do not reach for a broader token. |
| `fatal: Authentication failed` | The stored login is stale. The user runs `gh auth refresh` or `gh auth login` again. |
| `ssh: connect to host github.com port 22: Connection refused` | Try SSH over the HTTPS port: add a `Host github.com` entry with `Port 443` and `Hostname ssh.github.com` to `~/.ssh/config`. |
| Credentials not persisting | Only `gh` storage or the OS keychain are acceptable stores. Check `gh auth status`; if the machine has no keychain, the user completes `gh auth login` in their own session on that machine. |
| Multiple GitHub accounts | Use `gh auth switch` between `gh` logins, or SSH with a different key per host alias in `~/.ssh/config`. One account's credential is never copied into another's config by the agent. |
