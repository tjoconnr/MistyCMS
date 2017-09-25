#!/usr/bin/env python
from datetime import date,datetime
import json
import time
import logging

from google.appengine.ext import ndb as db

from ..utils import date_pretty

class BaseModel(db.Model):
    created_on = db.DateTimeProperty(required=True,auto_now_add=True)
    created_by = db.StringProperty(required=True,default="system")
    modified_on = db.DateTimeProperty(required=True,auto_now_add=True)
    modified_by = db.StringProperty(required=True,default="system")

    def save(self, user_id=None, modified_by="system"):
        self.modified_on = datetime.now()
        self.modified_by = modified_by
        return self.put()

    def to_dict(self):
        SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
        output = {}
        output["id"] = self.key.id()
        # output["created_on_human"] = utils.date_pretty(self.created_on)
        # output["modified_human"] = "Modified by '%s' on %s " % (self.modified_by, utils.date_pretty(self.modified_on))

        for key in dir(self):
            value = getattr(self, key)
            if key.find("_") != 0 and key.find("token") == -1: # Ensure not a built-in property or a sensitive auth token
                if isinstance(value, SIMPLE_TYPES) and value:
                    if isinstance(value, list) and not all(isinstance(x,(int,unicode,str,float)) for x in value):
                        if type(value[0]) == db.Key:
                            if value[0].id():
                                output[key] = [i.id() for i in value]
                            else:
                                output[key] = [i.name() for i in value]
                        else:
                            logging.info('Cannot encode list value "%s" of type "%s"' % (value[0], type(value[0])))
                    else:
                        output[key] = value
                elif isinstance(value, date):
                    # Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
                    ms = time.mktime(value.utctimetuple()) * 1000
                    ms += getattr(value, 'microseconds', 0) / 1000
                    output[key] = int(ms)
                elif isinstance(value, db.GeoPt):
                    output[key] = {'lat': value.lat, 'lon': value.lon}
                elif isinstance(value, BaseModel):
                    output[key] = value.to_dict()
                else:
                    pass #logging.info('Cannot encode key "%s" of type "%s"' % (key, type(value)))
        return output

    def to_json(self, pretty=True):
        if pretty:
            return json.dumps(self.to_dict(),sort_keys=True,indent=5)
        else:
            return json.dumps(self.to_dict())

