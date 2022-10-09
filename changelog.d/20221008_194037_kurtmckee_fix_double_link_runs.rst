Fixed
-----

-   Fix a bug that caused dotbot's Link plugin to run twice.

    This happened because dotbot's plugin loader detected the Link plugin class
    at the module level of the dotbot-firefox plugin and considered it a new plugin.
