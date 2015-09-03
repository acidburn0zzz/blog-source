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
THEME="./themes/bootstrap2"

# URL settings
ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html" 
PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

# Feeds settings 
FEED_ATOM = "feeds/feed.atom.xml"
FEED_ALL_ATOM = "feeds/feed.atom.all.xml" 
CATEGORY_FEED_ATOM = "feeds/feed.%s.xml"
FEED_RSS = "feeds/feed.rss.xml"
FEED_ALL_RSS = "feeds/feed.rss.all.xml"
CATEGORY_FEED_RSS = "feeds/feed.rss.%s.xml"

MD_EXTENSIONS = [
		'codehilite(linenums=False, guess_lang=True, noclasses=True, pygments_style=monokai)',
		'smarty',
        'extra']

# Blogroll
LINKS = (
		('Source!', 'https://github.com/wxcafe/blog-source', 'code'),
		('Public Git', 'http://git.wxcafe.net', 'github-sign'),
		)

# Social
SOCIAL = (
		('Twitter', 'https://twitter.com/wxcafe', 'twitter'),
		('Github', 'https://github.com/wxcafe', 'github'),
		('Email', 'mailto://wxcafe@wxcafe.net', 'envelope'),
		('Gpg', 'https://pub.wxcafe.net/wxcafe.asc', 'key'),
        ('IRL', 'https://www.openstreetmap.org/relation/105146', 'map-marker')
		)

# Categories on right-side bar but not on top menu
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_BAR = True
