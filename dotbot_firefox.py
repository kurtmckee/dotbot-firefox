# dotbot-firefox -- Configure your Firefox profile(s) using dotbot.
# Copyright 2022 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT


from __future__ import annotations

import logging
import os
import pathlib
import sys
import typing

from dotbot.plugin import Plugin
from dotbot.plugins.link import Link

__version__ = "1.0.0"

VALID_DIRECTIVES: set[str] = {"firefox"}

log = logging.getLogger(__name__)


def _get_profile_directories() -> typing.Iterable[pathlib.Path]:
    """Yield Firefox profile directories that appear to be valid."""

    defaults: list[str] = []

    if sys.platform.startswith("win32"):  # Windows
        defaults.append("${APPDATA}/Mozilla/Firefox/Profiles")
    elif sys.platform.startswith("darwin"):  # MacOS
        defaults.append("~/Library/Application Support/Firefox/Profiles")
    else:
        defaults.append("~/.mozilla/firefox")

        # When Firefox is installed and run as a snap,
        # it stores its profile info under $SNAP_USER_COMMON.
        #
        # It might be more correct to introspect $SNAP_USER_COMMON,
        # in case it's been customized, using a command like:
        #
        #     snap run --shell firefox -c 'echo $SNAP_USER_COMMON'
        #
        # ...but that seems unnecessary, and may be fragile and insecure.
        #
        snap_user_common = "~/snap/firefox/common"
        defaults.append(f"{snap_user_common}/.mozilla/firefox")

    for default in defaults:
        path = pathlib.Path(os.path.expandvars(os.path.expanduser(default)))
        if not path.is_dir():
            continue

        for profile in path.glob("*"):
            if profile.is_dir() and (profile / "prefs.js").is_file():
                yield profile


class Firefox(Plugin):
    def can_handle(self, directive: str) -> bool:
        """
        Flag whether this plugin supports the given *directive*.
        """

        return directive in VALID_DIRECTIVES

    def handle(self, directive: str, data: dict[str, typing.Any]) -> bool:
        """
        Handle Firefox configuration directives.

        :raises ValueError:
            ValueError is raised if `handle()` is called with an unsupported directive.
        """

        if not self.can_handle(directive):
            message = f"The Firefox plugin does not handle the '{directive}' directive."
            raise ValueError(message)

        success: bool = True

        if "user.js" in data:
            success &= self._handle_user_js(data["user.js"])

        return success

    def _handle_user_js(self, value: typing.Any) -> bool:
        """Create links to a specified ``user.js`` in each Firefox profile directory."""

        link_plugin = Link(self._context)
        links: dict[str, typing.Any] = {
            str(profile / "user.js"): value for profile in _get_profile_directories()
        }

        if not links:
            log.warning("No Firefox profiles found")
            return True

        return link_plugin.handle("link", links)
