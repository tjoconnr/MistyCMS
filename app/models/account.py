#!/usr/bin/env python
from google.appengine.ext import ndb as db
from google.appengine.api import memcache

from ._model import BaseModel

from app.constants import CACHE_SECONDS, ADMIN_SLUG

class Account(BaseModel):
    name = db.StringProperty(required=True)
    website = db.StringProperty(default="")
    is_active = db.BooleanProperty(default=False)

    @staticmethod
    def get_system_account():
        return Account.get_account(ADMIN_SLUG)

    @staticmethod
    def get_cache_key(account_id):
        return "account:%s" % account_id

    @staticmethod
    def get_account(account_id, force_refresh=False):
        CACHE_KEY = Account.get_cache_key(account_id)
        cached_account = memcache.get(CACHE_KEY)
        if cached_account != None and force_refresh == False:
            return cached_account
        db_account = Account.get_by_id(account_id)
        if db_account:
            memcache.add(CACHE_KEY, db_account, CACHE_SECONDS)
            return db_account
        return None

    @staticmethod
    def update(account_id, name, website):
        CACHE_KEY = Account.get_cache_key(account_id)

        account = Account.get_by_id(account_id)
        account.name = name
        account.website = website
        account.is_active = True
        account.save()

        memcache.delete(CACHE_KEY)
