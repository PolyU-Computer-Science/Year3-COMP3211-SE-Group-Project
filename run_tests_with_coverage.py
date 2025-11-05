import os
import sys
import unittest
from trace import Trace


def main():
    # Discover tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests')

    # Ensure coverage output dir
    out_dir = os.path.join('tests', 'coverage')
    os.makedirs(out_dir, exist_ok=True)

    tracer = Trace(count=True, trace=False, ignoremods=(
        'unittest', 'trace', 'importlib', 'encodings'
    ), infile=None, outfile=os.path.join(out_dir, 'coverage.txt'))

    # Run tests under tracer
    runner = unittest.TextTestRunner(verbosity=2)
    result = tracer.runfunc(runner.run, suite)

    # Produce report limited to model package
    results = tracer.results()
    # Write a summary and per-file .cover reports under tests/coverage
    results.write_results(show_missing=True, summary=True, coverdir=out_dir)

    print(
        f"\nCoverage report written to {out_dir}. Open the .cover files for per-file details.")
    # Exit code based on tests
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == '__main__':
    main()
