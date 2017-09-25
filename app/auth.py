#!/usr/bin/env python
import json
from google.appengine.api import users

from .constants import AUTH_LOGIN_URL, AUTH_LOGOUT_URL, AUTH_KNOWN_EMAILS, ENV
from .models import Account, User, Website
from .utils import gravatar

def create_user():
    email = users.get_current_user().email()
    username = email.split('@')[0].title()
    account_domain = email.split('@')[1].split('.')[0]

    # For business email, use the business name
    account_type = "free"
    account_name = username
    if account_domain not in AUTH_KNOWN_EMAILS:
        account_type = "startup"
        account_name = account_domain.split('.')[0].title()

    account = Account(name=account_name, account_type=account_type)
    account_key = account.save()

    user = User(id=email, name=username, account=account_key)
    user.save()
    return user
