# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import OnMaintenance
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import DECIMAL_PLACES


class kryptono (Exchange):

    def describe(self):
        return self.deep_extend(super(kryptono, self).describe(), {
            'id': 'kryptono',
            'name': 'Kryptono',
            'countries': ['SG'],
            'version': 'v2',
            'rateLimit': 1000,  # TODO: Check if self is the corrrect as per CCXT requirments. Kryptono gives 1000 minute intervals.
            'certified': True,  # TODO: Verify with Tony.
            # new metainfo interface
            'has': {
                'CORS': True,
                'fetchMarkets': True,
                'fetchCurrencies': True,
                'fetchTradingLimits': False,
                'fetchFundingLimits': False,
                'fetchTickers': True,  # TODO : Check with doc for fetchTicker
                'fetchOrderBook': True,
                'fetchTrades': True,
                'fetchOHLCV': True,
                'fetchBalance': True,
                'fetchTransactions': False,
                'withdraw': False,
                'desposit': False,
                'fetchDeposits': False,
                'fetchWithdrawals': False,
                'fetchDepositAddress': False,
                'fetchOrder': True,  # todo /api/v2/order/details
                'fetchOrders': True,  # todo  /api/v2/order/list/completed
                'fetchOpenOrders': True,  # todo /api/v2/order/list/open
                'fetchClosedOrders': False,  # todo api/v2/order/list/completed
                'fetchMyTrades': 'emulated',  # todo /api/v2/order/list/trades
            },
            'timeframes': {
                # TODO: Check if all of these intervals are supported.
                '1m': 'oneMin',
                '5m': 'fiveMin',
                '30m': 'thirtyMin',
                '1h': 'hour',
                '1d': 'day',
            },
            'hostname': 'p.kryptono.exchange/k',
            'urls': {
                'logo': 'https://storage.googleapis.com/kryptono-exchange/frontend/Kryptono%20Exchange.svg',
                'api': {
                    'market': 'https://api.kryptono.exchange/v1',
                    'v1': 'https://engine2.kryptono.exchange/api/v1',
                    'v2': 'https://p.kryptono.exchange/k/api/v2',
                },
                'test': {
                    'market': 'https://api.kryptono.exchange/v1',
                    'v1': 'https://engine-test.kryptono.exchange/api/v1',
                    'v2': 'https://testenv1.kryptono.exchange/k/api/v2',
                },
                'www': 'https://p.kryptono.exchange/k/home',
                'doc': [
                    'https://p.kryptono.exchange/k/api',
                ],
                'fees': [
                    'https://kryptono.zendesk.com/hc/en-us/articles/360004347772-2-Fee-on-Kryptono-Exchange-',
                ],
            },
            'api': {
                'v2': {
                    'get': [
                        'exchange-info',
                        'market-price',
                        # these endpoints require self.apiKey + self.secret
                        'account/balances',
                        'account/details',
                        'order/details',
                        'order/list/all',
                        'order/list/open',
                        'order/list/completed',
                        'order/list/trades',
                        'order/trade-detail',
                    ],
                },
                'market': {
                    'get': [
                        'getmarketsummaries',
                    ],
                },
                'v1': {
                    'get': [
                        'cs',
                        'dp',
                        'ht',
                    ],
                },
            },
            # todo Trading API Information in `https://kryptono.exchange/k/api#developers-guide-api-v2-for-kryptono-exchange-july-13-2018`
            'exceptions': {
                # 'Call to Cancel was throttled. Try again in 60 seconds.': DDoSProtection,
                # 'Call to GetBalances was throttled. Try again in 60 seconds.': DDoSProtection,
                # 'APISIGN_NOT_PROVIDED': AuthenticationError,
                # 'INVALID_SIGNATURE': AuthenticationError,
                # 'INVALID_CURRENCY': ExchangeError,
                # 'INVALID_PERMISSION': AuthenticationError,
                # 'INSUFFICIENT_FUNDS': InsufficientFunds,
                # 'QUANTITY_NOT_PROVIDED': InvalidOrder,
                # 'MIN_TRADE_REQUIREMENT_NOT_MET': InvalidOrder,
                # 'ORDER_NOT_OPEN': OrderNotFound,
                # 'INVALID_ORDER': InvalidOrder,
                # 'UUID_INVALID': OrderNotFound,
                # 'RATE_NOT_PROVIDED': InvalidOrder,  # createLimitBuyOrder('ETH/BTC', 1, 0)
                # 'WHITELIST_VIOLATION_IP': PermissionDenied,
                # 'DUST_TRADE_DISALLOWED_MIN_VALUE': InvalidOrder,
                # 'RESTRICTED_MARKET': BadSymbol,
                # 'We are down for scheduled maintenance, but we\u2019ll be back up shortly.': OnMaintenance,  # {"success":false,"message":"We are down for scheduled maintenance, but we\u2019ll be back up shortly.","result":null,"explanation":null}
            },
            'options': {
                'parseOrderStatus': False,
                'hasAlreadyAuthenticatedSuccessfully': False,  # a workaround for APIKEY_INVALID
                'symbolSeparator': '_',
                # With certain currencies, like
                # AEON, BTS, GXS, NXT, SBD, STEEM, STR, XEM, XLM, XMR, XRP
                # an additional tag / memo / payment id is usually required by exchanges.
                # With Bittrex some currencies imply the "base address + tag" logic.
                # The base address for depositing is stored on self.currencies[code]
                # The base address identifies the exchange as the recipient
                # while the tag identifies the user account within the exchange
                # and the tag is retrieved with fetchDepositAddress.
                'tag': {
                    'NXT': True,  # NXT, BURST
                    'CRYPTO_NOTE_PAYMENTID': True,  # AEON, XMR
                    'BITSHAREX': True,  # BTS
                    'RIPPLE': True,  # XRP
                    'NEM': True,  # XEM
                    'STELLAR': True,  # XLM
                    'STEEM': True,  # SBD, GOLOS
                    # https://github.com/ccxt/ccxt/issues/4794
                    # 'LISK': True,  # LSK
                },
                'subaccountId': None,
                # see the implementation of fetchClosedOrdersV3 below
                'fetchClosedOrdersMethod': 'fetch_closed_orders_v3',
                'fetchClosedOrdersFilterBySince': True,
            },
        })

    def cost_to_precision(self, symbol, cost):
        return self.decimal_to_precision(cost, TRUNCATE, self.markets[symbol]['precision']['price'], DECIMAL_PLACES)

    def fee_to_precision(self, symbol, fee):
        return self.decimal_to_precision(fee, TRUNCATE, self.markets[symbol]['precision']['price'], DECIMAL_PLACES)

    async def fetch_markets(self, params={}):
        response = await self.v2GetExchangeInfo(params)
        symbols = self.safe_value(response, 'symbols')
        # they mislabeled quotes to base
        quotes = self.safe_value(response, 'base_currencies')
        minQuotesMap = {}
        for i in range(0, len(quotes)):
            minQuotesMap[quotes[i]['currency_code']] = {
                'min': quotes[i]['minimum_total_order'],
                'max': None,
            }
        base = self.safe_value(response, 'coins')
        minBaseMap = {}
        for i in range(0, len(base)):
            minBaseMap[base[i]['currency_code']] = {
                'min': base[i]['minimum_order_amount'],
                'max': None,
            }
        result = []
        for i in range(0, len(symbols)):
            [base, quote] = symbols[i]['symbol'].split(self.options['symbolSeparator'])
            result.append({
                'id': symbols[i]['symbol'],
                'symbol': base + '/' + quote,
                'base': base,
                'baseId': base,
                'quote': quote,
                'quoteId': quote,
                'active': symbols[i]['allow_trading'],
                'info': symbols[i],
                'precision': {
                    'amount': symbols[i]['amount_limit_decimal'],
                    'price': symbols[i]['price_limit_decimal'],
                },
                'limits': {
                    'amount': {
                        'min': minBaseMap[base].min if minBaseMap[base] else None,
                        'max': None,
                    },
                    'price': {
                        'min': minQuotesMap[quote].min if minQuotesMap[quote] else None,
                        'max': None,
                    },
                },
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.v2GetAccountBalances(params)
        result = response.reduce(
            (finalResult, asset) => {
                finalResult[asset['currency_code']] = {
                    'free': asset.available,
                    'used': asset.in_order,
                    'total': asset.total,
                }
                return finalResult
            },
            {'info': response}
        )
        return self.parse_balance(result)

    async def fetch_order(self, id, symbol=None, params={}):
        request = {
            'order_id': id,
            'timestamp': self.milliseconds(),
        }
        request.recvWindow = params.recvWindow if params.recvWindow else 5000

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': symbol,
        }
        response = await self.v1GetDp(self.extend(request, params))
        #
        # {
        #     "symbol" : "KNOW_BTC",
        #     "limit" : 100,
        #     "asks" : [
        #       [
        #         "0.00001850",   # price
        #         "69.00000000"   # size
        #       ]
        #     ],
        #     "bids" : [
        #       [
        #         "0.00001651",       # price
        #         "11186.00000000"    # size
        #       ]
        #     ]
        #     "time" : 1529298130192
        #   }
        #
        return self.parse_order_book(response, response.time)

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "MarketName":"KNOW-BTC",
        #         "High":0.00001313,
        #         "Low":0.0000121,
        #         "BaseVolume":24.06681016,
        #         "Last":0.00001253,
        #         "TimeStamp":"2018-07-10T07:44:56.936Z",
        #         "Volume":1920735.0486831602,
        #         "Bid":"0.00001260",
        #         "Ask":"0.00001242",
        #         "PrevDay":0.00001253
        #       }
        #
        timestamp = self.parse8601(self.safe_string(ticker, 'TimeStamp'))
        symbol = None
        marketId = self.safe_string(ticker, 'MarketName')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                symbol = self.parseSymbol(marketId)
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        previous = self.safe_float(ticker, 'PrevDay')
        last = self.safe_float(ticker, 'Last')
        change = None
        percentage = None
        if last is not None:
            if previous is not None:
                change = last - previous
                if previous > 0:
                    percentage = (change / previous) * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'High'),
            'low': self.safe_float(ticker, 'Low'),
            'bid': self.safe_float(ticker, 'Bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'Ask'),
            'askVolume': None,
            'vwap': None,
            'open': previous,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'Volume'),
            'quoteVolume': self.safe_float(ticker, 'BaseVolume'),
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.marketGetGetmarketsummaries(params)
        #
        # {
        #     "success": "true",
        #     "message": "",
        #     "result": [
        #       {
        #         "MarketName":"KNOW-BTC",
        #         "High":0.00001313,
        #         "Low":0.0000121,
        #         "BaseVolume":24.06681016,
        #         "Last":0.00001253,
        #         "TimeStamp":"2018-07-10T07:44:56.936Z",
        #         "Volume":1920735.0486831602,
        #         "Bid":"0.00001260",
        #         "Ask":"0.00001242",
        #         "PrevDay":0.00001253
        #       },
        #       {
        #         "MarketName":"KNOW-ETH",
        #         "High":0.00018348,
        #         "Low":0.00015765,
        #         "BaseVolume":244.82775523,
        #         "Last":0.00017166,
        #         "TimeStamp":"2018-07-10T07:46:47.958Z",
        #         "Volume":1426236.4862518935,
        #         "Bid":"0.00017663",
        #         "Ask":"0.00017001",
        #         "PrevDay":0.00017166,
        #       },
        #       ...
        #     ],
        #     "volumes": [
        #       {
        #         "CoinName":"BTC",
        #         "Volume":571.64749041
        #       },
        #       {
        #         "CoinName":"KNOW",
        #         "Volume":19873172.0273
        #       }
        #     ],
        #     "t": 1531208813959
        #   }
        #
        result = self.safe_value(response, 'result')
        tickers = []
        for i in range(0, len(result)):
            ticker = self.parse_ticker(result[i])
            tickers.append(ticker)
        return self.filter_by_array(tickers, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.marketGetGetmarketsummaries(self.extend(request, params))
        #
        # {
        #     "success": "true",
        #     "message": "",
        #     "result": [
        #       {
        #         "MarketName":"KNOW-BTC",
        #         "High":0.00001313,
        #         "Low":0.0000121,
        #         "BaseVolume":24.06681016,
        #         "Last":0.00001253,
        #         "TimeStamp":"2018-07-10T07:44:56.936Z",
        #         "Volume":1920735.0486831602,
        #         "Bid":"0.00001260",
        #         "Ask":"0.00001242",
        #         "PrevDay":0.00001253
        #       },
        #       {
        #         "MarketName":"KNOW-ETH",
        #         "High":0.00018348,
        #         "Low":0.00015765,
        #         "BaseVolume":244.82775523,
        #         "Last":0.00017166,
        #         "TimeStamp":"2018-07-10T07:46:47.958Z",
        #         "Volume":1426236.4862518935,
        #         "Bid":"0.00017663",
        #         "Ask":"0.00017001",
        #         "PrevDay":0.00017166,
        #       },
        #       ...
        #     ],
        #     "volumes": [
        #       {
        #         "CoinName":"BTC",
        #         "Volume":571.64749041
        #       },
        #       {
        #         "CoinName":"KNOW",
        #         "Volume":19873172.0273
        #       }
        #     ],
        #     "t": 1531208813959
        #   }
        #
        ticker = response['result'][0]
        return self.parse_ticker(ticker, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        # await self.load_markets()
        # market = self.market(symbol)
        # request = {
        #     'symbol': symbol,
        #}
        # response = await self.v1GetHt(self.extend(request, params))
        #
        # {
        # "symbol":"KNOW_BTC",
        # "limit":100,
        # "history":[
        #     {
        #     "id":139638,
        #     "price":"0.00001723",
        #     "qty":"81.00000000",
        #     "isBuyerMaker":false,
        #     "time":1529262196270
        #     }
        #],
        # "time":1529298130192
        #}
        #
        # if 'history' in response:
        #     if response['history'] is not None:
        #         history = response.history.map(item =>({...item, 'timestamp': item.time}))
        #         return self.parse_trades(history, market, since, limit)
        #     }
        #}
        # raise ExchangeError(self.id + ' fetchTrades() returned None response')

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['T'] + '+00:00')
        return [
            timestamp,
            ohlcv['O'],
            ohlcv['H'],
            ohlcv['L'],
            ohlcv['C'],
            ohlcv['V'],
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        # https://engine2.kryptono.exchange/api/v1/cs?symbol=BTC_USDT&tt=1m
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'tickInterval': self.timeframes[timeframe],
            'marketName': market['id'],
        }
        response = await self.v1GetCs(self.extend(request, params))
        if 'result' in response:
            if response['result']:
                return self.parse_ohlcvs(response['result'], market, timeframe, since, limit)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.implode_params(self.urls['api'][api], {
            'hostname': self.hostname,
        }) + '/'
        if api != 'v2' and api != 'v3' and api != 'v3public':
            url += self.version + '/'
        if path.includes('account'):
            self.check_required_credentials()
            url += path
            query = self.urlencode(self.extend({
                'timestamp': self.milliseconds(),
                'recvWindow': self.options['recvWindow'],
            }, params))
            signature = self.hmac(self.encode(query), self.encode(self.secret))
            url += '?' + query
            headers = {
                'Authorization': self.apiKey,
                'Signature': signature,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            }
        elif path.includes('order'):
            #  todo we may be able to combine with 'account' part of if statement above if body can be signed similarly
        else:  # public endpoints
            url += path
            if params:
                url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        # a workaround for APIKEY_INVALID
        if (api == 'account') or (api == 'market'):
            self.options['hasAlreadyAuthenticatedSuccessfully'] = True
        return response