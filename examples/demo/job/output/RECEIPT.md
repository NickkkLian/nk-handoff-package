# Hand-back receipt

## What I did
Wrote output/work/slugify.py and two unit tests for the one-line spec.

## How I verified it
`python3 -B test_slugify.py` in output/work: 2 tests, raw output in output/evidence/unit-tests.txt.

## Unsure
Non-ASCII letters (for example accented ones) become "-" because the spec says non-alphanumerics; I did not test that.

## Boundary crossings
none
