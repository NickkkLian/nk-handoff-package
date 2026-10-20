"""The generated entry point must use its relocated bundled runner."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import handoff_init
import make_verifier


class PortabilityTests(unittest.TestCase):
    def test_relocated_delivery_and_external_anchor(self):
        with tempfile.TemporaryDirectory() as temp:
            original = Path(temp) / 'original'
            package = Path(handoff_init.scaffold(str(original), 'handoff'))
            (package / 'reference/spec.md').write_text('Synthetic input.\n')
            handoff_init.seal(str(package))
            handoff_init.fill_demo(str(package))
            handoff_init.trust_root(str(package), str(original / 'anchor.txt'))
            make_verifier.install(original)
            delivery = Path(temp) / 'delivery'
            shutil.move(str(original), delivery)
            # Run from a different cwd, using the generated verifier's own location.
            result = subprocess.run([sys.executable, '-B', str(delivery / 'verify.py')], cwd=temp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('planned 3 / ran 3 / failed 0', result.stdout)
            self.assertNotIn(str(original), (delivery / 'verify.py').read_text())
            (delivery / 'handoff/output/handback_check.py').write_text('print("ALL PASS")\n')
            result = subprocess.run([sys.executable, '-B', str(delivery / 'verify.py')], cwd=temp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn('mismatch:', result.stdout)
            self.assertIn('handback_check.py', result.stdout)


if __name__ == '__main__':
    unittest.main()
