#!/usr/bin/env python
from google.appengine.ext import ndb as db
from ._model import BaseModel

from ..constants import CACHE_SECONDS, ADMIN_SLUG, ASSET_TYPES

class Asset(BaseModel):
    account = db.KeyProperty(kind="Account", required=True)
    name = db.StringProperty(required=True)
    asset_type = db.StringProperty(required=True, choices=ASSET_TYPES)
    content = db.TextProperty()
    is_public = db.BooleanProperty(default=False)

    @staticmethod
    def list(account_id):
        q = Asset.query(
            db.OR(
                Asset.account == db.Key("Account", account_id),
                Asset.account == db.Key("Account", ADMIN_SLUG)
            )
        )
        return q.fetch(None)
