import os
from datetime import datetime
from flask import session
from collections import deque

__author__ = 'Surfer'


def brackify(tag):
    return '<%s>' % tag


def taggify(html, tags):
    balanced_tags = deque([html])
    for tag in tags:
        balanced_tags.appendleft(brackify(tag))
        balanced_tags.append(brackify('/%s' % tag))
    return ''.join(balanced_tags)


def mark_as_preformatted(html):
    return taggify(html, ['pre', 'code'])


def calc_expiration():
    timeout = os.environ.get('SESSION_TIMEOUT')
    if not timeout:
        timeout = 10
    else:
        timeout = int(timeout)
    return datetime.now() + datetime.timedelta(seconds=timeout)


def check_logged_in():
    if session.get('logged_in'):
        if datetime.now() <= session['expiration']:
            session['expiration'] = calc_expiration()
            return True
    return False
