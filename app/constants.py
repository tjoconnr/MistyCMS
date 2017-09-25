#!/usr/bin/env python

ENV = {
    'name': 'Misty',
    'icon': 'heart',
    'description': 'Build Remarkable Websites',
    'admin': '/a',
    'signup': '/signup',
    'login': '/login'
}

ACCOUNT_TYPES = ["free", "personal", "startup", "ultimate"]
ADMIN_SLUG = 'sys'
ASSET_TYPES = ["theme", "template"]
POST_TYPES = ["index", "page", "post"]
POST_STATUS = ["draft", "review", "publish", "private"]
CACHE_SECONDS = 60*60

AUTH_LOGIN_URL = '/authorize'
AUTH_LOGOUT_URL = '/'
AUTH_KNOWN_EMAILS = ["gmail"]
