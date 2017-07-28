#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Misc Settings
AUTHOR = u'wxcafé'
SITENAME = u'Wxcafé'
SITEURL = '//wxcafe.net'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'fr'
DEFAULT_PAGINATION = 10
THEME="./themes/pelican-clean-blog"
HEADER_COVER = SITEURL + '/theme/cover.png'
COLOR_SCHEME_CSS = 'monokai.css'

# URL settings
ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"
PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

# Feeds settings
FEED_RSS = "feeds/feed.rss.xml"
FEED_ATOM = "feeds/feed.atom.xml"
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_ALL_ATOM = None

MD_EXTENSIONS = [
        'codehilite(linenums=False, guess_lang=True, noclasses=True, pygments_style=monokai)',
        'smarty',
        'extra']

# Social
SOCIAL = (
        ('twitter', 'https://twitter.com/wxcafe'),
        ('pencil-square-o', 'https://social.wxcafe.net/@wxcafe'),
        ('github', 'https://github.com/wxcafe'),
        ('envelope', 'mailto://wxcafe@wxcafe.net'),
        ('key', 'https://pub.wxcafe.net/wxcafe.asc'),
        ('map-o', 'https://www.openstreetmap.org/relation/105146'),
        ('code', 'https://github.com/wxcafe/blog-source'),
        )

# Categories on right-side bar but not on top menu
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_BAR = True
