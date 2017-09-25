#!/usr/bin/env python
from google.appengine.ext import ndb as db
from google.appengine.api import memcache

from ._model import BaseModel
from ..constants import CACHE_SECONDS

class Website(BaseModel):
    account = db.KeyProperty(kind="Account", required=True)
    name = db.StringProperty(required=True)
    description = db.StringProperty()
    subdomain = db.StringProperty()
    title = db.StringProperty()
    template = db.KeyProperty(kind="Asset")
    theme = db.KeyProperty(kind="Asset")


    @staticmethod
    def update(website_id, account_id, name, description, subdomain, title):
        if website_id:
            website = Website.get_by_id(long(website_id))
        else:
            website = Website(account=db.Key("Account", account_id))

        website.name = name
        website.description = description
        website.subdomain = subdomain
        website.title = title
        return website.save()
        memcache.set("site:%s" % subdomain, website, CACHE_SECONDS)

    @staticmethod
    def get_website(website_id):
        if website_id:
            return Website.get_by_id(long(website_id))

    @staticmethod
    def get_website_by_domain(subdomain):
        CACHE_KEY = "site:%s" % subdomain
        cached_site = memcache.get(CACHE_KEY)
        if cached_site != None:
            return cached_site

        db_site = Website.get_by_id(subdomain)
        if db_site != None:
            memcache.add(CACHE_KEY, db_site, CACHE_SECONDS)
            return db_site

        raise Exception('Site not found: %s' % subdomain)

    @staticmethod
    def list(account_id):
        q = Website.query().filter(Website.account == db.Key("Account", account_id))
        return q.fetch(10)

class WebsiteMeta(BaseModel):
    website = db.KeyProperty(kind="Website", required=True)
    meta_key = db.StringProperty(required=True)
    meta_value = db.StringProperty(required=True)
