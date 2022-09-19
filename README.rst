..  dotbot-firefox -- Configure your Firefox profile(s) using dotbot.
..  Copyright 2022 Kurt McKee <contactme@kurtmckee.org>
..  SPDX-License-Identifier: MIT


dotbot-firefox
##############

Configure your Firefox profile(s) using `dotbot`_.

-------------------------------------------------------------------------------


Table of contents
=================

*   `What you can do with it`_
*   `Installation`_
*   `Configuration`_
*   `Firefox profile locations`_
*   `Development`_


What you can do with it
=======================

When Firefox starts, it will look for a ``user.js`` file in your profile directory.
If found, the ``user.js`` settings will be copied to ``prefs.js`` and used.

You can enforce a consistent Firefox configuration across all your profiles
by using dotbot-firefox to create symlinks to a custom ``user.js``.
The plugin will find Firefox profile directories that contain a ``prefs.js`` file
and will use dotbot's builtin Link plugin to create the symlinks.


Installation
============

There are two ways to install and use the plugin:

1.  Install it as a Python package.
2.  Add it as a git submodule in your dotfiles repository.
3.  Copy ``dotbot_firefox.py`` into your dotfiles directory.


Python package
--------------

If you want to install dotbot-firefox as a Python package
(for example, if you're using a virtual environment),
then you can install the plugin using ``pip``:

..  code-block::

    pip install dotbot-firefox

Then, when running dotbot, use the ``-p`` or ``--plugin`` option
to tell dotbot to load the plugin:

..  code-block::

    dotbot [...] --plugin dotbot_firefox [...]

If you're using one of dotbot's ``install`` scripts,
you'll need to edit that file to add the ``--plugin`` option.


Git submodule
-------------

If you want to track dotbot-firefox as a git submodule
(for example, if you manage your dotfiles using git)
then you can add the plugin repository as a submodule using ``git``:

..  code-block::

    git submodule add https://github.com/kurtmckee/dotbot-firefox.git

This will clone the repository to a directory named ``dotbot-firefox``.
Then, when running dotbot, use the ``-p`` or ``--plugin`` option
to tell dotbot to load the plugin:

..  code-block::

    dotbot [...] --plugin dotbot-firefox/dotbot_firefox.py [...]

Note that you may need to initialize the plugin's git submodule
when you clone your dotfiles repository or pull new changes
to another computer.
The command for this will look something like:

..  code-block::

    git submodule update --init dotbot-firefox


Copy ``dotbot_firefox.py``
--------------------------

If desired, you can copy ``dotbot_firefox.py`` to your dotfiles directory.
You might choose to do this if you already use other plugins
and have configured dotbot to load all plugins from a plugin directory.

If you copy ``dotbot_firefox.py`` to the root of your dotfiles directory
then, when running dotbot, use the ``-p`` or ``--plugin`` option
to tell dotbot to load the plugin:

..  code-block::

    dotbot [...] --plugin dotbot_firefox.py [...]

If you copy ``dotbot_firefox.py`` to a directory containing other plugins,
you can use dotbot's ``--plugin-dir`` option to load all plugins in the directory.
In the example below, the plugin directory is named ``dotbot-plugins``:

..  code-block::

    dotbot [...] --plugin-dir dotbot-plugins [...]


Configuration
=============

First, create a ``user.js`` file in the dotfiles directory that dotbot manages.
For example, it could contain this configuration to set your homepage:

..  code-block:: js

    user_pref("browser.startup.homepage", "https://dashboard.example");

(MozillaZine maintains an extensive list of `Firefox configuration settings`_.)

Then, add a ``firefox`` directive to your dotbot config with a ``user.js`` key.
The value of the key follows the syntax of the `dotbot Link plugin`_.

..  code-block:: yaml

    # Example 1:
    # "user.js" can be specified as a string.
    firefox:
      user.js: firefox/user.js


    # Example 2:
    # "user.js" can have no value, and will be found
    # in the same directory as your dotbot config file.
    firefox:
      user.js:


    # Example 3:
    # The extended Link plugin syntax is supported.
    firefox:
      user.js:
        path: firefox/user.js
        force: true


Firefox profile locations
=========================

The dotbot-firefox plugin is aware of the following default directories:

*   ``%APPDATA%\Mozilla\Firefox\Profiles`` (Windows)
*   ``~/Library/Application Support/Firefox/Profiles`` (Mac OS)
*   ``~/.mozilla/firefox`` (Linux)
*   ``~/snap/firefox/common/.mozilla/firefox`` (Firefox Snap for Linux)

Only profile subdirectories that contain a ``prefs.js`` file
will be considered valid by the plugin.


Development
===========

To set up a development environment, clone the dotbot-firefox plugin's git repository.
Then, follow these steps to create a virtual environment and run the unit tests locally:

..  code-block:: shell

    # Create the virtual environment
    $ python -m venv .venv

    # Activate the virtual environment (Linux)
    $ . .venv/bin/activate

    # Activate the virtual environment (Windows)
    $ & .venv/Scripts/Activate.ps1

    # Update pip and setuptools, and install wheel
    (.venv) $ pip install -U pip setuptools wheel

    # Install poetry
    (.venv) $ pip install poetry

    # Install all dependencies
    (.venv) $ poetry install

    # Run the unit tests locally
    (.venv) $ tox


..  Links
..  =====
..
..  _dotbot: https://github.com/anishathalye/dotbot
..  _dotbot Link plugin: https://github.com/anishathalye/dotbot#link
..  _Firefox configuration settings: https://kb.mozillazine.org/About:config_entries
