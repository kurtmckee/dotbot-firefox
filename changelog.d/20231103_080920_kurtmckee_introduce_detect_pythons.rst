Updated
-------

*   Require dotbot 1.20.1 or higher.

Development
-----------

*   Rewrite the test suite to rely on requirements files.
*   Introduce an ``update`` label in the tox config that will update requirements files
    as well as pre-commit hook and additional dependency versions.
*   Colorize tox, pytest, and mypy output when running locally and in CI.
