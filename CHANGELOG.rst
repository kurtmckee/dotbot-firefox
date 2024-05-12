..  dotbot-firefox -- Configure your Firefox profile(s) using dotbot.
..  Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
..  SPDX-License-Identifier: MIT


dotbot-firefox
##############

Unreleased changes
==================

Unreleased changes to the code are documented in
`changelog fragments <https://github.com/kurtmckee/dotbot-firefox/tree/main/changelog.d/>`_
in the ``changelog.d/`` directory on GitHub.

..  scriv-insert-here

.. _changelog-1.1.0:

1.1.0 — 2023-05-23
==================

Python support
--------------

-   Add support for Python 3.12.

Added
-----

-   Support Firefox Flatpak for Linux profile directories.

.. _changelog-1.0.1:

1.0.1 — 2022-10-08
==================

Fixed
-----

-   Fix a bug that caused dotbot's Link plugin to run twice.

    This happened because dotbot's plugin loader detected the Link plugin class
    at the module level of the dotbot-firefox plugin and considered it a new plugin.

.. _changelog-1.0.0:

1.0.0 — 2022-10-08
==================

Added
-----

-   Support a ``"firefox"`` directive that will configure a user's Firefox profile(s).
-   Support a ``"user.js"`` configuration key.

    The plugin will search all known system-specific default profile directories
    and will use dotbot's built-in Link plugin to create ``user.js`` symlinks
    in each profile directory that contains a ``prefs.js`` file.
