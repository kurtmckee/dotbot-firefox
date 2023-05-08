# dotbot-firefox -- Configure your Firefox profile(s) using dotbot.
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import os
import pathlib
import sys
import typing

import dotbot.plugin
import dotbot.plugins.link

__version__ = "1.0.1"

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

        snap_user_common = "~/snap/firefox/common"
        defaults.append(f"{snap_user_common}/.mozilla/firefox")

    for default in defaults:
        path = pathlib.Path(os.path.expandvars(os.path.expanduser(default)))
        if not path.is_dir():
            continue

        for profile in path.glob("*"):
            if profile.is_dir() and (profile / "prefs.js").is_file():
                yield profile


class Firefox(dotbot.plugin.Plugin):
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

        if "userChrome.css" in data or "chrome" in data:
            user_chrome_value = data.get("userChrome.css", data.get("chrome"))
            success &= self._handle_user_chrome(user_chrome_value)

        return success

    def _handle_user_js(self, value: typing.Any) -> bool:
        """Create links to a specified ``user.js`` in each Firefox profile directory."""

        link_plugin = dotbot.plugins.link.Link(self._context)
        links: dict[str, typing.Any] = {
            str(profile / "user.js"): value for profile in _get_profile_directories()
        }

        if not links:
            log.warning("No Firefox profiles found")
            return True

        return link_plugin.handle("link", links)

    def _handle_user_chrome(self, value: typing.Any) -> bool:
        """Link userChrome.css or chrome directory in each Firefox profile directory."""
        success = True

        if isinstance(value, str):
            src = pathlib.Path(os.path.expandvars(os.path.expanduser(value)))

            if src.is_file() and src.name == "userChrome.css":
                link_plugin = dotbot.plugins.link.Link(self._context)
                links = {
                    str(profile / "chrome" / "userChrome.css"): value
                    for profile in _get_profile_directories()
                }
                success &= link_plugin.handle("link", links)
            elif src.is_dir() and src.name == "chrome":
                link_plugin = dotbot.plugins.link.Link(self._context)
                for profile in _get_profile_directories():
                    chrome_dst = profile / "chrome"
                    links = {
                        str(chrome_dst / f.relative_to(src)): str(f)
                        for f in src.glob("**/*")
                        if f.is_file()
                    }
                    success &= link_plugin.handle("link", links)
            else:
                log.error(
                    f"Invalid path for userChrome.css or chrome directory: {value}"
                )
                success = False

        return success
