#!/usr/bin/env python
from google.appengine.ext import ndb as db
from google.appengine.api import memcache

from ._model import BaseModel
from app.constants import CACHE_SECONDS

class Menu(BaseModel):
    account = db.KeyProperty(kind="Account", required=True)
    name = db.StringProperty(required=True)
    template = db.KeyProperty(kind="Asset")
    theme = db.KeyProperty(kind="Asset")
    css = db.TextProperty()
    rendered = db.TextProperty()

    @staticmethod
    def get_rendered(menu_id):
        CACHE_KEY = "menu-rendered:%s" % menu_id
        return memcache.get(CACHE_KEY)

    @staticmethod
    def set_rendered(menu_id, html):
        CACHE_KEY = "menu-rendered:%s" % menu_id
        memcache.add(CACHE_KEY, html, CACHE_SECONDS)

    @staticmethod
    def get_menu(menu_id):
        menu_id = long(menu_id)

        CACHE_KEY = "menu:%s" % menu_id

        cached_menu = memcache.get(CACHE_KEY)
        if cached_menu != None:
            return cached_menu

        db_menu = Menu.get_by_id(menu_id)
        if db_menu != None:
            memcache.add(CACHE_KEY, db_menu, CACHE_SECONDS)
            return db_menu

        return None

    @staticmethod
    def list(account_id):
        q = Menu.query().filter(Menu.account == db.Key("Account", account_id))
        return q.fetch(None)


class MenuItem(BaseModel):
    menu = db.KeyProperty(kind="Menu", required=True)
    name = db.StringProperty(required=True)
    description = db.StringProperty()
    category = db.StringProperty()
    price = db.FloatProperty(default=0.0)

    @staticmethod
    def list(menu_id):
        q = MenuItem.query().filter(MenuItem.menu == db.Key("Menu", menu_id))
        return q.fetch(None)

