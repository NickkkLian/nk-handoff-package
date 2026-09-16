# nk-handoff-package

A [Claude Code](https://code.claude.com) skill. Hand a line of work to an executor that has no context — another agent, a contractor, a future session — so that the work comes back checkable.

Part of [nickkk-skills](https://github.com/NickkkLian/nickkk-skills) — skills that stop an AI coding agent's
"done, tested, safe" from being taken on faith.

![nk-handoff-package demo: before and after](https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/nk-handoff-package.gif)

## What it does

- `handoff_init.py` scaffolds the package (boundary as orders, sealed read-only reference layer, output layer with evidence and pending-sync templates, receipt with an "unsure" section), seals it, and pins a trust root outside it.
- `handback_check.py` is the generic hand-back check both sides run: three exit states, templates exempt by hash, project gates as a plugin, an empty package fails.
- `handoff_verify.py` is the acceptor's runner with a declared denominator: trust root, self-check on a copy, drift vs the true source; NOT RUN is never a pass.

The full procedure, the boundaries and where the rules came from are in [SKILL.md](SKILL.md).

## How it works

1. `python3 scripts/handoff_init.py <workspace> <task> [--form full|round|asset]` Refuses to touch a non-empty package
2. Put the inputs in `reference/` and seal
3. Write `output/project_gates.py` for anything project-specific (thresholds, required files, forbidden imports)
4. Pin the trust root outside the package
5. Keep your acceptance material outside too (this file, the trust root, expected answers)

## Install

Pick one of three ways. Skills load when a session starts, so open a **new** session after installing.

### 1 · Terminal, one command

```bash
git clone https://github.com/NickkkLian/nk-handoff-package ~/.claude/skills/nk-handoff-package
```

1. Run the command above (for one project only, clone into `.claude/skills/nk-handoff-package` inside that project).
2. Start a new Claude Code session.
3. Check it loaded: type `/nk-handoff-package` — it appears in the slash-command menu. Or just ask for the task; the skill triggers on its own.

### 2 · Claude Code in a terminal session (plugin)

The plugin route goes through the [nickkk-skills](https://github.com/NickkkLian/nickkk-skills) marketplace. Add it once; after that each skill is one command.

```
/plugin marketplace add NickkkLian/nickkk-skills
/plugin install nk-handoff-package@nickkk-skills
```

1. In a Claude Code session, run the first line (once per machine).
2. Run the second line.
3. Start a new session (or run `/reload-plugins`). The skill shows up as `nk-handoff-package:nk-handoff-package`.

Without opening a session, the same two steps work from a shell: `claude plugin marketplace add NickkkLian/nickkk-skills` then `claude plugin install nk-handoff-package@nickkk-skills`.

### 3 · Claude desktop app (Code tab)

**Add the marketplace first — Discover only searches marketplaces you have already added.**

<img src="https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/panel-route/panel-route.gif" alt="Adding the marketplace and installing a skill in the desktop app" width="640">

<sub>The repository list in this recording shows the recorder's own repositories because a GitHub account is connected; yours will show yours. Type the full name as in step 4.</sub>

1. In the chat box, type `/plugin marketplace` and press Enter (or open **Settings → Customize → Plugins**). The **Plugins** panel opens.
   <br><img src="https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/panel-route/step1-type-plugin-marketplace.png" alt="/plugin marketplace typed in the chat box" width="480">
2. Top right, open **Add ▾** and choose **Add marketplace**.
   <br><img src="https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/panel-route/step2-add-menu.png" alt="The Add menu with Add marketplace" width="480">
3. Choose **Add from a repository**.
   <br><img src="https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/panel-route/step3-add-from-repository.png" alt="Add marketplace dialog: Add from a repository" width="480">
4. In **URL**, type the full `NickkkLian/nickkk-skills`. At the bottom of the list choose the row **Use "NickkkLian/nickkk-skills"**, then press **Sync**.
   <br><img src="https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/panel-route/step4-url-then-sync.png" alt="URL filled in, Sync button" width="480">
5. You land on **Discover**, filtered to the new marketplace (**Filter · 1**). Find **Nk handoff package** and press **Add**. Installed ones show **✓ Added**.
   <br><img src="https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/panel-route/step5-discover-add.png" alt="Discover list with Added and Add buttons" width="480">
6. Close the panel and start a new session.

To try it for one session without installing anything: `claude --plugin-dir ./nk-handoff-package` from a clone.

## Verify

```bash
python3 scripts/handback_check.py --selftest
python3 scripts/handoff_init.py --selftest
python3 scripts/handoff_verify.py --selftest
```

Standard library only, Python 3.9+. Before publishing, the guarded lines of each script were
mutated one at a time in a sandbox copy and the self-test was confirmed to go red on the named
assertion, without a traceback; the unmutated control stayed green.

## Limits

- The checks read shapes (a `$` line, a filled section, a hash). A plausible fabrication passes; the auditor and the evidence exist for that reason.
- Without `--source`, drift only proves the executor did not alter its inputs, not that the inputs are current.

## License

MIT. Read a script before letting it run in your environment.
