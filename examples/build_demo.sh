#!/bin/sh
# Rebuilds examples/demo/ from scratch: a tiny synthetic hand-back (task: write slugify()), already filled in the way an
# executor would, sealed, with its trust root pinned OUTSIDE the package. No personal data; nothing outside examples/ is written.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")
d="$here/demo"
rm -rf "$d"; mkdir -p "$d"
python3 "$root/scripts/handoff_init.py" "$d" job --form round >/dev/null
p="$d/job"

cat > "$p/reference/spec.md" <<'SPEC'
slugify(text): lower-case, runs of non-alphanumerics become one "-", no leading or trailing "-".
SPEC
python3 "$root/scripts/handoff_init.py" "$d" job --seal >/dev/null

cat > "$p/START.md" <<'T'
# START: slugify demo

## Step 0 - the boundary
Your write scope is this package. Do not write outside it, do not push to any remote: a push would not fail, it
would silently overwrite another line of work.

## Step 1 - read reference/spec.md (the whole spec, one line)
## Step 2 - nothing else to read
## Step 3 - completeness check: `cd output && python3 handback_check.py` runs; before you work it must FAIL.

## What you hand back
output/work/ (the code), output/evidence/ (re-run command, then raw output), output/pending/ (records), RECEIPT.md
(with a filled Unsure section). Before handing back: `cd output && python3 handback_check.py`, exit 0.
T
cat > "$p/TASK.md" <<'T'
# This round
Goal: implement slugify(text) as reference/spec.md says.
Deliverable: output/work/slugify.py and output/work/test_slugify.py.
Not changing: reference/.
Do not: edit output/handback_check.py or output/project_gates.py.
T

cat > "$p/output/work/slugify.py" <<'T'
import re


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
T
cat > "$p/output/work/test_slugify.py" <<'T'
import unittest
from slugify import slugify


class T(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_runs_and_edges(self):
        self.assertEqual(slugify("  a -- b  "), "a-b")


if __name__ == "__main__":
    unittest.main()
T
{
  echo '$ cd output/work && python3 -B test_slugify.py'
  (cd "$p/output/work" && python3 -B test_slugify.py 2>&1; echo "exit=$?")
} > "$p/output/evidence/unit-tests.txt"

cat > "$p/output/RECEIPT.md" <<'T'
# Hand-back receipt

## What I did
Wrote output/work/slugify.py and two unit tests for the one-line spec.

## How I verified it
`python3 -B test_slugify.py` in output/work: 2 tests, raw output in output/evidence/unit-tests.txt.

## Unsure
Non-ASCII letters (for example accented ones) become "-" because the spec says non-alphanumerics; I did not test that.

## Boundary crossings
none
T
cat > "$p/output/pending/commit-messages/slugify.md" <<'T'
# Add slugify()

Why: the demo task needs a URL-safe slug.
Verified by: python3 -B test_slugify.py (output/evidence/unit-tests.txt)
T
echo '{"date": "2026-10-22", "kind": "minor", "note": "added slugify()"}' > "$p/output/pending/devlog/slugify.jsonl"

# pin the trust root OUTSIDE the package (next to it, not inside job/)
python3 "$root/scripts/handoff_init.py" "$d" job --trust-root "$d/trust-root.txt" >/dev/null
echo "built $d"
