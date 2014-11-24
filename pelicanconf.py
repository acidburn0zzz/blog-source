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
ARTICLE_URL = "posts/{date:%D}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%D}/{slug}/index.html" 
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

# Blogroll
LINKS = (
		('Source!', 'https://github.com/wxcafe/blog-source', 'code'),
		('Zerobin', 'http://paste.wxcafe.net', 'paste'),
		('Public Git', 'http://git.wxcafe.net', 'github-sign'),
		)

# Social
SOCIAL = (
		('Twitter', 'https://twitter.com/wxcafe', 'twitter'),
		('Github', 'https://github.com/wxcafe', 'github'),
		('Email', 'mailto://wxcafe@wxcafe.net', 'envelope'),
		('Gpg', 'https://data.wxcafe.net/wxcafe.asc', 'key'),
		('Finger', 'finger://wxcafe@wxcafe.net', 'terminal'),
		('IRL', 'http://leloop.org/where.html', 'map-marker')
		)

# Categories on right-side bar but not on top menu
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_BAR = True
