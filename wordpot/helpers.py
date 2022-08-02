#!/usr/bin/env python

from flask import request
from wordpot import app
from wordpot.logger import LOGGER

# -----------------
# Plugins whitelist
# -----------------

def is_plugin_whitelisted(plugin):
    # If PLUGINS option doesn't exist allow all
    return (
        'PLUGINS' in app.config
        and plugin in app.config['PLUGINS']
        or 'PLUGINS' not in app.config
    )

# ----------------
# Themes whitelist
# ----------------

def is_theme_whitelisted(theme):
    if 'THEMES' not in app.config:
        return True
        # Theme is in the whitelist
    return theme in app.config['THEMES'] or theme == app.config['THEME']
