Testing
=======

ALWAYS WRITE AND RUN TESTS BEFORE YOU COMMIT TO THE MASTER BRANCH.

Write tests as you are writing the code – it helps you catch invariants and
corner cases you might forget about later.

Tests are *especially* important when/if you do any **bug fixes**. Create a
test that makes sure the bug is fixed. This will be of great help later on when
refactoring, so nobody accidentally creates the same bug again.


Running and making tests
------------------------

In the working directory of memery, the entire test suite can be run with

    $ python3 tests.py

All modules should have tests contained in the file `test_<module>.py`. All
such test modules should have a method `test_run_all()` that runs all tests for
that module. When you add a new module, modify `tests.py` so that it also runs your
module's `test_run_all()` function.


Test logging
------------

The `tests.py` module provides a `Logger` object which can (and should?) be
used to log what the tests are testing for. It has two methods:

 1. `logger.print(msg)` which prints the message neatly, and
 2. `logger.deeper(part)` which creates a new logger that can be used by some
    other test, deeper in the hierarchy

See the existing testing modules for further usage information.

