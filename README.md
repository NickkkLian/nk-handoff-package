# nk-handoff-package

An agent skill for [Claude Code](https://code.claude.com) and [OpenAI Codex](https://developers.openai.com/codex). Hand a line of work to an executor that has no context — another agent, a contractor, a future session — so that the work comes back checkable.

**What you get.** A hand-back you can accept or refuse. Below, the acceptor's runner on a small synthetic package ([examples/demo/](examples/demo/): a one-line task, "write `slugify()`", handed back with tests, evidence and a receipt). Then the same package after the executor swapped the hand-back checker for `print("ALL PASS")`. Both runs are real output, copied on 2026-10-22 from a clone of this repository.

```text
$ python3 scripts/handoff_verify.py examples/demo/job --trust-root examples/demo/trust-root.txt
  ✔ trustroot  PASS     5 pinned files match
  ✔ selfcheck  PASS     exit 0
planned 2 / ran 2 / failed 0
next: dispatch an independent auditor on output/evidence/ (this runner is not the audit)
$ echo $?
0
```

```text
$ cp -R examples/demo/job /tmp/job-tampered
$ echo 'print("ALL PASS")' > /tmp/job-tampered/output/handback_check.py
$ python3 scripts/handoff_verify.py /tmp/job-tampered --trust-root examples/demo/trust-root.txt
  ✘ trustroot  FAIL     mismatch: ['output/handback_check.py'] — nothing the package says about itself counts until this is explained
  ✔ selfcheck  PASS     exit 0
planned 2 / ran 2 / failed 1
next: dispatch an independent auditor on output/evidence/ (this runner is not the audit)
--- raw handback_check output ---
ALL PASS
$ echo $?
1
```

The replaced checker still exits 0 ("selfcheck PASS"): a package cannot vouch for itself. Only the hashes kept outside it (`trust-root.txt`) show that the checker is not the one that was shipped, and the runner exits 1. Exit 0 means the declared steps passed, not that the work is correct: the runner says so itself in its `next:` line, and a hand-back whose code is wrong but whose evidence file looks right is also accepted (see Limits). In the first run, the lines after the `next:` line (a "--- raw handback_check output ---" marker, then the raw output of the 19 gate checks, all passing) are left out; run the command to see them. The demo package was built in one go by [examples/build_demo.sh](examples/build_demo.sh), so its trust root was pinned after it was filled in; in real use you pin it before you hand the package out.

![nk-handoff-package](https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/social/nk-handoff-package.png)

Part of [nickkk-skills](https://github.com/NickkkLian/nickkk-skills) — skills that stop an AI coding agent's
"done, tested, safe" from being taken on faith.

## Try it

Nothing is installed and nothing under `~/.claude` changes: clone, run the self-test, run the example (it only writes inside the clone).

```bash
git clone https://github.com/NickkkLian/nk-handoff-package && cd nk-handoff-package
python3 scripts/handback_check.py --selftest
python3 scripts/handoff_init.py --selftest
python3 scripts/handoff_verify.py --selftest
python3 -B scripts/make_verifier.py --selftest
python3 scripts/handoff_verify.py examples/demo/job --trust-root examples/demo/trust-root.txt
python3 scripts/handoff_init.py demo job --form round
```

The self-tests print:

```text
handback_check selftest · 10/10 passed
handoff_init selftest · 9/9 passed
handoff_verify selftest · 8/8 passed
make_verifier selftest: 3/3 passed (relocated success, tamper rejection, no absolute lab path)
```

The verify command prints the first run at the top of this page (exit code 0). The last command only scaffolds an empty package: it prints `scaffolded <full path of your clone>/demo/job (form round). Next: fill every '<<< FILL' slot, put inputs in reference/, then --seal and --trust-root.` and its exit code is 0. That is setup, not a result.

![nk-handoff-package demo: before and after](https://raw.githubusercontent.com/NickkkLian/nickkk-skills/main/gallery/nk-handoff-package.gif)

## What it does

- `handoff_init.py` scaffolds the package (boundary as orders, sealed read-only reference layer, output layer with evidence and pending-sync templates, receipt with an "unsure" section), seals it, and pins a trust root outside it.
- `handback_check.py` is the generic hand-back check both sides run: three exit states, templates exempt by hash, project gates as a plugin, an empty package fails.
- `handoff_verify.py` is the acceptor's runner with a declared denominator: trust root, self-check on a copy, drift vs the true source; NOT RUN is never a pass.

The full procedure, the boundaries and where the rules came from are in [SKILL.md](SKILL.md).

## How it works

1. `python3 scripts/handoff_init.py <workspace> <task> [--form full|round|asset]` Refuses to touch a non-empty package.
2. Put the inputs in `reference/` and seal: `handoff_init.py <workspace> <task> --seal`.
3. Write `output/project_gates.py` for anything project-specific (thresholds, required files, forbidden imports).
4. Pin the trust root outside the package: `handoff_init.py <workspace> <task> --trust-root`.
5. Keep your acceptance material outside too (this file, the trust root, expected answers).

## Why it is built this way

**The idea.** The hard part of delegating is not copying the files; it is moving the discipline with them, and making the result checkable by someone who was not there.

**Where it came from.** Own practice, 2026-09: five delegations of whole projects to an outside agent, two of them cross-reviewed for eight rounds each; a trust root added after three in-package ways of turning red into green were measured; a stop rule added after an eleven-round audit loop.

**Evidence.** What was broken on purpose to show that the self-tests can fail is under [Verify](#verify); what was run end to end, and in which agent, is under [Compatibility](#compatibility).

## Portable acceptor entry point — 2026-10-20

For the repaired workflow: when the task uses `handoff/` and an external `anchor.txt`, run
`python3 scripts/make_verifier.py /path/to/project`. Deliver `verify.py` and `acceptor-tools/` together beside
`handoff/`; keep those acceptor files and `anchor.txt` outside the folder writable by the executor. The entry point
resolves its bundled runner relative to itself. It requires no lab checkout or machine-specific absolute path.
The relocated fixture passes 9/9 original mechanical checks in three recorded re-scorings; these are not new model runs.

## Measured comparison — 2026-10-20

**TOOL on this benchmark.** Plain Codex and plain Claude received the ordinary task prompt on the same cases and pinned inputs, without the benchmark skill. Both a Codex judge and a Claude judge assessed the artifacts using the native rubric and randomized blind labels. All three arms passed the full mechanical task 3/3; the measured advantage is in judged quality.

| Arm | Original full passes | QA full passes | Original mean score | Codex judge | Claude judge | Agent seconds |
| --- | --- | --- | --- | --- | --- | --- |
| Repaired skill | 3/3 | 3/3 | 1.0000 | 0.9545 | 0.9848 / 1.0000 | n/a (recorded run) |
| Plain Codex | 3/3 | 3/3 | 1.0000 | 0.6667 | 0.6667 | 484.9 |
| Plain Claude | 3/3 | 3/3 | 1.0000 | 0.6818 | 0.6970 | 598.2 |

The judged criteria include features the plain prompt was never asked for (a receipt with an "Unsure" section, one evidence file per claim, `pending/` records, and, partly, the planned/ran/failed count), so this table shows what the skill adds, not that a plain agent fails at the same task. Plain agents also caught a swapped checker (the prompt asked for a fingerprint file kept outside the package), and all three arms passed the mechanical task 3/3.

Claude judge skill means are separate for the Codex-pair and Claude-pair contexts. These are paired ratings, not one pooled skill mean.

The skill arm is one repaired recorded artifact re-scored three times, not three independent model generations. The original handoff threshold requires a quality delta of at least 3/11. Only a clear win over both baselines under both judges qualifies as TOOL. No speed advantage is claimed: the skill row's "Agent seconds" is n/a because its package was not made live in this comparison. It is the recorded output of an agent run of skill 0.1.0 (gpt-5.6-sol, low reasoning, 2026-09-16), replayed and re-scored, so there is no run time to set against the 484.9 and 598.2 seconds the plain arms took. The small sample (n=3), task reuse, recognizable templates, same-family judges, paired judging contexts, different run dates and different agent caps limit generalization. Other tasks, models, agent versions and installation routes were not retested in this release job. The compatibility table below is historical, not a fresh compatibility claim. See [EVIDENCE.md](EVIDENCE.md) and [the measured records](evidence/cross-agent-2026-10-20.json) for settings and per-case ratings.

## Install

Pick one of four ways: three for Claude Code, one for OpenAI Codex. Skills load when a session starts, so open a **new** session after installing.

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

<sub>Recorded on 2026-09-16, when the marketplace listed ten skills, all at version 0.1.0; it lists more now. The repository list in this recording shows the recorder's own repositories because a GitHub account is connected; yours will show yours. Type the full name as in step 4.</sub>

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

### 4 · OpenAI Codex CLI

```bash
git clone https://github.com/NickkkLian/nk-handoff-package.git ~/.agents/skills/nk-handoff-package
```

1. Run the command above (for one project only, clone into `.agents/skills/nk-handoff-package` inside that project).
2. Start a new Codex session.
3. Check it loaded, without spending a model call: `codex debug prompt-input | grep -o -- '- nk-handoff-package[a-z0-9:-]*' | sort -u` prints `- nk-handoff-package:nk-handoff-package:`. Codex adds the `nk-handoff-package:` prefix because this repository also carries a Claude Code plugin manifest. Ask for the task and the skill triggers on its own, or type `$` and pick it from the list.

## Compatibility

| Agent | Tested | What was checked |
|---|---|---|
| Claude Code (CLI 2.1.173, macOS) | yes | In a fresh project with an isolated Claude config, inside a macOS sandbox that blocked reading the tester's ~/.claude folder (settings, session history, memory), Desktop, Documents and Downloads, SSH keys and git identity, a plain request that never names the skill triggered it and it ran its bundled script. The route 2 plugin commands were also run from a shell with an isolated config: marketplace add, install, list. |
| OpenAI Codex CLI (0.154.0-alpha.6.2, gpt-5.6-sol, low reasoning, macOS) | yes | Copied into `~/.agents/skills` of a temporary home (the folder route 4 clones into), in a fresh project, without the user's Codex config. From a plain request that never names the skill, Codex read SKILL.md, built the package with `scripts/handoff_init.py`, sealed it, pinned the trust root outside it and ran `scripts/handoff_verify.py`: planned 3, ran 3, failed 1, as expected before any work is handed back. |
| Cursor, Gemini CLI | no | Not tested. Their documentation says both read `~/.agents/skills`, the folder route 4 clones into; Gemini CLI asks before it activates a skill. |

In this skill's Codex run, every call into the skill folder's scripts/ used that folder's absolute path. Route 4 was checked for this repository: cloned from GitHub into a temporary home's `~/.agents/skills`, it was listed by the step 3 command. This skill's frontmatter uses only name, description, license and metadata.

## Verify

```bash
python3 scripts/handback_check.py --selftest
python3 scripts/handoff_init.py --selftest
python3 scripts/handoff_verify.py --selftest
python3 -B scripts/make_verifier.py --selftest
```

Standard library only, Python 3.9+. The original three scripts passed their self-tests on 2026-09-30, and
`breakcheck.py` from [nk-breakable-selftest](https://github.com/NickkkLian/nk-breakable-selftest) broke each script on purpose in a sandbox copy:

- `handback_check.py`: 3 lines broken one at a time; 1 turned the self-test red without a traceback. Not covered: the self-test stayed green with L132, L214 switched off.
- `handoff_init.py`: 2 lines broken one at a time; each turned the self-test red without a traceback.
- `handoff_verify.py`: 1 line broken one at a time; it turned the self-test red without a traceback.

The unmutated control stayed green every time. Only lines that record a finding, raise, or return a failing exit code
were broken (the tool's pattern, or the hand-written list); a line number refers to the script as shipped in this version.
This shows those lines are covered. It does not show that nothing else can fail.

Release checks on 2026-10-20: all four script self-tests and the relocation regression pass. A deliberate broken bundled-runner path makes the portable self-test fail; restoring the original bytes passes again. Raw commands and output: [release checks](evidence/release-tests.txt), [break check](evidence/break-check.txt). Run the focused regression with `python3 -B -W ignore::ResourceWarning -m unittest discover -s tests -v`; the warning filter applies only to inherited handoff helpers that still use temporary file handles without context managers.

## Limits

- The checks read shapes (a `$` line, a filled section, a hash). A plausible fabrication passes; the auditor and the evidence exist for that reason.
- Without `--source`, drift only proves the executor did not alter its inputs, not that the inputs are current.

## Privacy

This skill's scripts run on your computer, started by you or by the agent you use it in. `handoff_init.py` writes files and folders only in the workspace folder you name (put it inside your own project) and, with `--seal`, records a hash of each file you put in `reference/`. `make_verifier.py` writes only into the delivery folder you name. `handoff_verify.py` copies the package you name into a temporary folder, runs the package's own scripts there (`output/handback_check.py`, which can load `output/project_gates.py`; both are code written by whoever filled the package, so run the verifier only on packages you trust), and deletes the copy; with `--source` it also reads and hashes the source folder you name. Nothing is sent anywhere: the scripts open no network connection and read no environment variable. The agent you run the skill in sends your conversation, including what the scripts print, to its own model provider under your own sign-in; this skill does not. The author keeps no data.

## License

MIT. Read a script before letting it run in your environment.
