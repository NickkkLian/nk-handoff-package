"""The README's first screen is a real run of examples/demo; this test re-runs it and checks the quoted lines."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / 'scripts' / 'handoff_verify.py'
DEMO = ROOT / 'examples' / 'demo'
MISMATCH = ("  ✘ trustroot  FAIL     mismatch: ['output/handback_check.py'] "
            "— nothing the package says about itself counts until this is explained")


def verify(package):
    return subprocess.run([sys.executable, '-B', str(VERIFY), str(package), '--trust-root', str(DEMO / 'trust-root.txt')],
                          capture_output=True, text=True)


class DemoTests(unittest.TestCase):
    def test_demo_is_accepted_and_tampered_copy_refused(self):
        ok = verify(DEMO / 'job')
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertIn('planned 2 / ran 2 / failed 0', ok.stdout)
        with tempfile.TemporaryDirectory() as temp:
            bad = Path(temp) / 'job'
            shutil.copytree(DEMO / 'job', bad)
            (bad / 'output' / 'handback_check.py').write_text('print("ALL PASS")\n')
            r = verify(bad)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(MISMATCH, r.stdout)
        self.assertIn('planned 2 / ran 2 / failed 1', r.stdout)
        self.assertIn('  ✔ selfcheck  PASS     exit 0', r.stdout)   # the replaced checker itself still says pass

    def test_readme_quotes_what_the_runner_prints(self):
        readme = (ROOT / 'README.md').read_text()
        for line in (MISMATCH, 'next: dispatch an independent auditor on output/evidence/ (this runner is not the audit)', 'planned 2 / ran 2 / failed 0', 'planned 2 / ran 2 / failed 1',
                     '  ✔ trustroot  PASS     5 pinned files match'):
            self.assertIn(line, readme)


if __name__ == '__main__':
    unittest.main()
