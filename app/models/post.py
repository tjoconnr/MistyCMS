#!/usr/bin/env python
from google.appengine.ext import ndb as db
from google.appengine.api import memcache

from ._model import BaseModel
from ..constants import CACHE_SECONDS, POST_TYPES

class PostMeta(BaseModel):
    post = db.KeyProperty(kind="Post", required=True)
    meta_key = db.StringProperty(required=True)
    meta_value = db.StringProperty(required=True)

class Post(BaseModel):
    website = db.KeyProperty(kind="Website", required=True)
    post_author = db.KeyProperty(kind="User", required=True)
    post_name = db.StringProperty(required=True)
    post_slug = db.StringProperty(required=True)
    post_type = db.StringProperty(required=True, choices=POST_TYPES)
    post_status = db.StringProperty(required=True, choices=POST_TYPES)
    post_theme = db.KeyProperty(kind="Asset")
    post_image = db.KeyProperty(kind="Media")
    post_is_noindex = db.BooleanProperty(default=False)
    post_is_nofollow = db.BooleanProperty(default=False)
    post_is_noarchive = db.BooleanProperty(default=False)
    post_seo_description = db.StringProperty()
    post_seo_title = db.StringProperty()
    post_seo_keywords = db.StringProperty()
    post_header_script = db.StringProperty()
    post_footer_script = db.StringProperty()

    def get_post_meta(self):
        return PostMeta.query().filter(PostMeta.post == self.id())

    @staticmethod
    def get_post(subdomain=None, slug=None):
        CACHE_KEY = "post:%s:%s" % (subdomain, slug)
        cached_post = memcache.get(CACHE_KEY)
        if cached_post != None:
            return cached_post

        db_post = Post.query().filter(Post.website == db.Key("Website", subdomain)).filter(Post.post_slug == slug).get()

        if db_post != None:
            memcache.add(CACHE_KEY, db_post, CACHE_SECONDS)
            return db_post

        raise Exception('Post not found: %s' % slug)

    @staticmethod
    def list(subdomain):
        q = Post.query().filter(Post.website == db.Key("Website", subdomain))
        return q.fetch(10)
