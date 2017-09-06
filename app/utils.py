#!/usr/bin/env python
def gravatar(email,img_size=100):
    import urllib, hashlib
    gravatar_url = "http://gravatar.com/avatar/"
    gravatar_url += hashlib.md5(email.lower()).hexdigest()
    gravatar_url += "?"
    gravatar_url += urllib.urlencode({
        's': img_size,
        'd': "mm",
    })
    return gravatar_url

def date_pretty(dt, dt_format='%B %d, %Y at %X UTC'):
    return dt.strftime(dt_format)
