#!/usr/bin/env python
from google.appengine.ext import ndb as db
from ._model import BaseModel

from app.constants import CACHE_SECONDS, ADMIN_SLUG, ASSET_TYPES

class Asset(BaseModel):
    account = db.KeyProperty(kind="Account", required=True)
    name = db.StringProperty(required=True)
    asset_type = db.StringProperty(required=True, choices=ASSET_TYPES)
    content = db.TextProperty()
    is_public = db.BooleanProperty(default=False)

    @staticmethod
    def get_asset(id, asset_type="template"):
        q = Asset.query().filter(Asset.asset_type == asset_type).filter(Asset.name == name)
        return q.fetch(1)[0]

    @staticmethod
    def get_assets(account_id):
        q = Asset.query(
            db.OR(
                Asset.account == db.Key("Account", account_id),
                Asset.account == db.Key("Account", ADMIN_SLUG)
            )
        )
        return q.fetch(100)
