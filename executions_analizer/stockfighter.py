#!/usr/bin/env python
import re
import sys
import requests


api_key = '52d0445bb4e4a5e4f7672d3701e55cef1bacc7e1'

def do_request(method, url, data=None, auth=False):
    if auth:
        headers = {'X-Starfighter-Authorization': api_key}
    else:
        headers = None

    r = requests.request(method, url, json=data, headers=headers)

    if r.status_code != 200:
        print r.status_code, r.reason, r.text, r.headers
        raise RuntimeError('HTTP {}: {}'.format(r.status_code, r.reason))

    result = r.json()

    if not result['ok']:
        print r.status_code, r.reason, r.text, r.headers
        raise RuntimeError(result['error'])

    return result


def api_request(method, path, data=None, auth=False):
    url = 'https://api.stockfighter.io/ob/api/' + path
    return do_request(method, url, data, auth)

def gm_request(method, path, data=None):
    url = 'https://www.stockfighter.io/gm/' + path
    return do_request(method, url, data, auth=True)


def api_get(path, auth=False):
    return api_request('GET', path, auth=auth)


def api_post(path, data):
    return api_request('POST', path, data, auth=True)


def api_delete(path):
    return api_request('DELETE', path, auth=True)


def check_api():
    return api_get('heartbeat')


def check_venue(venue):
    return api_get('venues/{}/heartbeat'.format(venue))


def get_symbols(venue):
    return api_get('venues/{}/stocks'.format(venue))


def get_snapshot(venue, symbol):
    return api_get('venues/{}/stocks/{}'.format(venue, symbol))


def get_quote(venue, symbol):
    return api_get('venues/{}/stocks/{}/quote'.format(venue, symbol))


def get_order_status(venue, symbol, order_id):
    return api_get('venues/{}/stocks/{}/orders/{}'.format(venue, symbol, order_id), auth=True)


def get_all_orders(venue, account):
    return api_get('venues/{}/accounts/{}/orders'.format(venue, account), auth=True)


def get_all_orders_in(venue, account, symbol):
    return api_get('venues/{}/accounts/{}/stocks/{}/orders'.format(venue, account, symbol), auth=True)


def place_order(account, venue, symbol, price, qty, direction, order_type):
    assert isinstance(price, int)
    assert isinstance(qty, int)
    assert direction in ['buy', 'sell']
    assert order_type in ['limit', 'market', 'fok', 'ioc']

    payload = {
        'account': account,
        'venue': venue,
        'stock': symbol,
        'price': price,
        'qty': qty,
        'direction': direction,
        'orderType': order_type
    }

    return api_post('venues/{}/stocks/{}/orders'.format(venue, symbol), data=payload)


def cancel_order(venue, symbol, order_id):
    result = api_delete('venues/{}/stocks/{}/orders/{}'.format(venue, symbol, order_id))
    assert not result['open']
    return result


def get_order_account(venue, symbol, order_id):
    path = 'venues/{}/stocks/{}/orders/{}'.format(venue, symbol, order_id)
    url = 'https://api.stockfighter.io/ob/api/' + path
    headers = {'X-Starfighter-Authorization': api_key}

    r = requests.request('DELETE', url, headers=headers)
    if r.status_code == 404:
        return None
    else:
        assert r.status_code == 401 or r.status_code == 200

    result = r.json()

    if result['ok']:
        return result['account']
    else:
        assert not result['ok']

        match = re.match(r'Not authorized to delete that order.  You have to own account (.+)\.', result['error'])
        assert match

        return match.group(1)
