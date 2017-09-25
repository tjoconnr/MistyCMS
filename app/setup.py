#!/usr/bin/env python
import logging

from .models import Account, Asset, Post, User, Website
from .constants import ADMIN_SLUG

DEFAULT_THEME = """
@import url('https://fonts.googleapis.com/css?family=Neucha');
body, .menu-item h1 {
  font-family: 'Neucha';
}"""

THEME_BLUE = """
@import url('https://fonts.googleapis.com/css?family=Poppins');

body {
  background: radial-gradient(rgba(23,62,84,0.9), #09101a);
}

body, .menu-item h1 {
  font-family: 'Poppins', cursive;
}"""

THEME_CURSIVE = """
@import url('https://fonts.googleapis.com/css?family=Dancing+Script');

body, .menu-item h1 {
  font-family: 'Dancing Script', cursive;
}"""

THEME_BREWERY = """
@import url('https://fonts.googleapis.com/css?family=Quicksand');
body {
  background: url(/static/img/hops.jpg) no-repeat;
  background-size: cover;
}

body, .menu-item h1 {
  font-family: 'Quicksand', cursive;
}"""

THEME_WHIMSY = """
@import url('https://fonts.googleapis.com/css?family=Princess+Sofia');
body, .menu-item h1 {
  font-family: 'Princess Sofia', cursive;
}"""

DEFAULT_TEMPLATE = """
{% extends "views/__master.html" %}
{% block body %}
<div class="container-fluid">
  <div class="menu-items">
    {% for m in menu_items %}
    <div class="menu-item">
      <h1>{{ m.name }}</h1>
      <h3>
        ABV: {{ m.description }}
        &bull;
        ${{ '{0:0.2f}'.format(m.price) }}
      </h3>
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
"""

TEMPLATE_FULL = """
{% extends "views/__master.html" %}
{% block body %}
<div class="container-fluid">
   <div class="page-header">
    <h2>{{ menu.name }} <small class="pull-right">{{ account.name }}</small></h2>
  </div>
  <div class="menu-items">
    {% for m in menu_items %}
    <div class="menu-item">
      <h1>{{ m.name }}</h1>
      <h3>
        ABV: {{ m.description }}
        &bull;
        ${{ '{0:0.2f}'.format(m.price) }}
      </h3>
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
"""

def create_default_assets():
    logging.info('create_default_assets()')

    admin_account = Account.get_by_id(ADMIN_SLUG)
    if admin_account:
        return

    admin_account = Account(id=ADMIN_SLUG, name="System", is_active=True)
    account_key = admin_account.save()

    theme = Asset(account=account_key, id="default", name="Default", asset_type="theme", content=DEFAULT_THEME)
    theme.save()

    theme = Asset(account=account_key, id="brewery", name="Brewery", asset_type="theme", content=THEME_BREWERY)
    theme.save()

    theme = Asset(account=account_key, id="cursive", name="Cursive", asset_type="theme", content=THEME_CURSIVE)
    theme.save()

    theme = Asset(account=account_key, id="blue", name="Blue", asset_type="theme", content=THEME_BLUE)
    theme.save()

    theme = Asset(account=account_key, id="whimsy", name="Whimsy", asset_type="theme", content=THEME_WHIMSY)
    theme.save()

    template = Asset(account=account_key, id="template-default", name="Default", asset_type="template", content=DEFAULT_TEMPLATE)
    template.save()

    template = Asset(account=account_key, id="template-full", name="Full", asset_type="template", content=TEMPLATE_FULL)
    template.save()
