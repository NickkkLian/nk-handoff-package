# nk-handoff-package

A [Claude Code](https://code.claude.com) skill. Hand a line of work to an executor that has no context — another agent, a contractor, a future session — so that the work comes back checkable.

Part of [nickkk-skills](https://github.com/NickkkLian/nickkk-skills) — skills that stop an AI coding agent's
"done, tested, safe" from being taken on faith.

## What it does

- `handoff_init.py` scaffolds the package (boundary as orders, sealed read-only reference layer, output layer with evidence and pending-sync templates, receipt with an "unsure" section), seals it, and pins a trust root outside it.
- `handback_check.py` is the generic hand-back check both sides run: three exit states, templates exempt by hash, project gates as a plugin, an empty package fails.
- `handoff_verify.py` is the acceptor's runner with a declared denominator: trust root, self-check on a copy, drift vs the true source; NOT RUN is never a pass.

The full procedure, the boundaries and where the rules came from are in [SKILL.md](SKILL.md).

## Install

Copy the folder into your skills directory (the skill is the repository root):

```bash
git clone https://github.com/NickkkLian/nk-handoff-package ~/.claude/skills/nk-handoff-package
```

or inside one project: `git clone … .claude/skills/nk-handoff-package`.

As a plugin, through the marketplace in the index repository:

```
/plugin marketplace add NickkkLian/nickkk-skills
/plugin install nk-handoff-package@nickkk-skills
```

To try it for one session without installing: `claude --plugin-dir ./nk-handoff-package`.

## Verify

```bash
python3 scripts/handback_check.py --selftest
python3 scripts/handoff_init.py --selftest
python3 scripts/handoff_verify.py --selftest
```

Standard library only, Python 3.9+. Before publishing, the guarded lines of each script were
mutated one at a time in a sandbox copy and the self-test was confirmed to go red on the named
assertion, without a traceback; the unmutated control stayed green.

## License

MIT. Read a script before letting it run in your environment.
