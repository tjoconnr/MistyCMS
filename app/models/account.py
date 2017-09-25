#!/usr/bin/env python
from google.appengine.ext import ndb as db
from google.appengine.api import memcache

from ._model import BaseModel

from ..constants import CACHE_SECONDS, ADMIN_SLUG, ACCOUNT_TYPES

def get_cache_key(account_id):
        return "account:%s" % account_id

class AccountUser(BaseModel):
    account = db.KeyProperty(kind="Account", required=True)
    user = db.KeyProperty(kind="User", required=True)

class Account(BaseModel):
    name = db.StringProperty(required=True)
    is_active = db.BooleanProperty(default=True)
    account_type = db.StringProperty(default=ACCOUNT_TYPES[0], choices=ACCOUNT_TYPES)

    @staticmethod
    def get_system_account():
        return Account.get_account(ADMIN_SLUG)

    @staticmethod
    def get_account(account_id, force_refresh=False):
        CACHE_KEY = get_cache_key(account_id)
        cached_account = memcache.get(CACHE_KEY)
        if cached_account != None and force_refresh == False:
            return cached_account
        db_account = Account.get_by_id(account_id)
        if db_account:
            memcache.add(CACHE_KEY, db_account, CACHE_SECONDS)
            return db_account
        return None

    @staticmethod
    def update(account_id, name, account_type):
        CACHE_KEY = get_cache_key(account_id)
        account = Account.get_by_id(account_id)
        account.name = name
        account.account_type = account_type
        account.save()
        memcache.set(CACHE_KEY, account, CACHE_SECONDS)
