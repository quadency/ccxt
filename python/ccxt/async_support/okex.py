# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.okcoinusd import okcoinusd


class okex (okcoinusd):

    def describe(self):
        return self.deep_extend(super(okex, self).describe(), {
            'id': 'okex',
            'name': 'OKEX',
            'countries': ['CN', 'US'],
            'has': {
                'CORS': False,
                'futures': True,
                'fetchTickers': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/32552768-0d6dd3c6-c4a6-11e7-90f8-c043b64756a7.jpg',
                'api': {
                    'v3': 'https://www.okex.com/v3',
                    'web': 'https://www.okex.com/v2',
                    'public': 'https://www.okex.com/api',
                    'private': 'https://www.okex.com/api',
                },
                'www': 'https://www.okex.com',
                'doc': [
                    'https://github.com/okcoin-okex/API-docs-OKEx.com',
                    'https://www.okex.com/docs/en/',
                ],
                'fees': 'https://www.okex.com/pages/products/fees.html',
                'referral': 'https://www.okex.com',
            },
            'fees': {
                'trading': {
                    'taker': 0.0015,
                    'maker': 0.0010,
                },
                'spot': {
                    'taker': 0.0015,
                    'maker': 0.0010,
                },
                'future': {
                    'taker': 0.0005,
                    'maker': 0.0002,
                },
                'swap': {
                    'taker': 0.00075,
                    'maker': 0.0002,
                },
            },
            'commonCurrencies': {
                # OKEX refers to ERC20 version of Aeternity(AEToken)
                'AE': 'AET',  # https://github.com/ccxt/ccxt/issues/4981
                'HOT': 'Hydro Protocol',
                'HSR': 'HC',
                'MAG': 'Maggie',
                'YOYO': 'YOYOW',
                'WIN': 'WinToken',  # https://github.com/ccxt/ccxt/issues/5701
            },
        })
