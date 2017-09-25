#!/usr/bin/env python
from google.appengine.ext import ndb as db
from google.appengine.api import memcache

from ._model import BaseModel
from ..constants import CACHE_SECONDS

USER_ROLES = ["user", "admin"]

class UserMeta(BaseModel):
    user = db.KeyProperty(kind="User", required=True)
    meta_key = db.StringProperty(required=True)
    meta_value = db.StringProperty(required=True)

class User(BaseModel):
    account = db.KeyProperty(kind="Account", required=True)
    name = db.StringProperty(required=True)
    is_active = db.BooleanProperty(default=True)
    profile = db.StringProperty(required=True, default=USER_ROLES[0], choices=USER_ROLES)

    @staticmethod
    def get_user(user_id, force_refresh=False):
        cached_user = memcache.get(user_id)
        if cached_user != None and force_refresh == False:
            return cached_user

        db_user = User.get_by_id(user_id)
        if db_user != None:
            memcache.add(user_id, db_user, CACHE_SECONDS)
            return db_user

    @staticmethod
    def update(user_id, name):
        user = User.get_by_id(user_id)
        user.name = name
        user.save()
        memcache.set(user_id, user, CACHE_SECONDS)
