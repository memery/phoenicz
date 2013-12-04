Testing
=======

ALWAYS WRITE AND RUN TESTS BEFORE YOU COMMIT TO THE MASTER BRANCH.

Write tests as you are writing the code – it helps you catch invariants and
corner cases you might forget about later.

In the working directory of memery, the entire test suite can be run with

    $ python3 tests.py

All modules should have tests contained in the file `test_<module>.py`. All
such test modules should have a method `test_run_all()` that runs all tests for
that module. When you add a new module, modify `test_<module>.py` so that it also runs your
module's `test_run_all()` function.

By convention, modules start their suite by printing

    [<module>]: Running all tests...

and end it with

    [<module>]: All tests complete!

Each actual test is prefaced with

    [<module>/<part>]: <Doing xxx>

where `<part>` is some sort of identifier for what part of `<module>` is
tested.

All this printing stuff could probably be a lot more automated...
