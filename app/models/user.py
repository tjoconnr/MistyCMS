#!/usr/bin/env python
from google.appengine.ext import ndb as db
from google.appengine.api import memcache

from ._model import BaseModel
from app.constants import CACHE_SECONDS

USER_ROLES = ["user", "admin"]

class User(BaseModel):
    account = db.KeyProperty(kind="Account", required=True)
    name = db.StringProperty(required=True)
    is_active = db.BooleanProperty(default=False)
    profile = db.StringProperty(required=True, default=USER_ROLES[0], choices=USER_ROLES)

    @staticmethod
    def get_user(email, force_refresh=False):
        cached_user = memcache.get(email)
        if cached_user != None and force_refresh == False:
            return cached_user
        db_user = User.get_by_id(email)
        if db_user != None:
            memcache.add(email, db_user, CACHE_SECONDS)
            return db_user
        return None

    @staticmethod
    def update(user_id, name):
        user = User.get_by_id(user_id)
        user.name = name
        user.is_active = True
        user.save()
        memcache.delete(user_id)
