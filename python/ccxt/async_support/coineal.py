# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound


class coineal(Exchange):

    def describe(self):
        return self.deep_extend(super(coineal, self).describe(), {
            'id': 'coineal',
            'name': 'Coineal',
            'countries': [],
            'rateLimit': 1000,
            'has': {
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOrderBook': True,
                'fetchTrades': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchBalance': True,
                'fetchOrder': True,
                'fetchClosedOrders': True,
                'fetchTicker': True,
            },
            'timeframes': {
                '1m': '1',  # default
                '5m': '5',
                '15m': '15',
                '30m': '30',
                '1h': '60',
                '1d': '1440',
            },
            'urls': {
                'api': {
                    'public': 'https://exchange-open-api.coineal.com',
                    'private': 'https://exchange-open-api.coineal.com',
                },
                'www': 'https://exchange-open-api.coineal.com',
            },
            'api': {
                'public': {
                    'get': [
                        'open/api/common/symbols',
                        'open/api/get_records',
                        'open/api/market_dept',
                        'open/api/get_trades',
                        'open/api/get_ticker',
                    ],
                },
                'private': {
                    'get': [
                        'open/api/all_trade',
                        'open/api/new_order',
                        'open/api/user/account',
                        'open/api/order_info',
                    ],
                    'post': [
                        'open/api/create_order',
                        'open/api/cancel_order',
                    ],
                },
            },
            'exceptions': {
                '5': InvalidOrder,
                '6': InvalidOrder,
                '7': InvalidOrder,
                '8': InvalidOrder,
                '19': InsufficientFunds,
                '22': OrderNotFound,
                '23': ArgumentsRequired,
                '24': ArgumentsRequired,
                '100004': BadRequest,
                '100005': BadRequest,
                '100007': AuthenticationError,
                '110002': BadSymbol,
                '110005': InsufficientFunds,
                '110032': AuthenticationError,
            },
            'errorMessages': {
                '5': 'Order Failed',
                '6': 'Exceed the minimum volume requirement',
                '7': 'Exceed the maximum volume requirement',
                '8': 'Order cancellation failed',
                '9': 'The transaction is frozen',
                '13': 'Sorry, the program has a system error, please contact the webmaster',
                '19': 'Insufficient balance available',
                '22': 'Order does not exist',
                '23': 'Missing transaction quantity parameter',
                '24': 'Missing transaction price parameter',
                '25': 'Quantity Precision Error',
                '100001': 'System error',
                '100002': 'System upgrade',
                '100004': 'Parameter request is invalid',
                '100005': 'Parameter signature error',
                '100007': 'Unathorized IP',
                '110002': 'Unknown currency code',
                '110005': 'Insufficient balance available',
                '110025': 'Account locked by background administrator',
                '110032': 'This user is not athorized to do self',
            },
        })

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        url += '/' + path
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            content = ''
            query['api_key'] = self.apiKey
            sortedParams = self.keysort(query)
            keys = list(sortedParams.keys())
            for i in range(0, len(keys)):
                key = keys[i]
                content += key + str(sortedParams[key])
            signature = content + self.secret
            hash = self.hash(self.encode(signature), 'md5')
            query['sign'] = hash
            if method == 'POST':
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
        if query:
            url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def fetch_markets(self, params={}):
        response = await self.publicGetOpenApiCommonSymbols()
        # Exchange response
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": [
        #         {
        #             "symbol": "btcusdt",
        #             "count_coin": "usdt",
        #             "amount_precision": 5,
        #             "base_coin": "btc",
        #             "price_precision": 2
        #         }
        #     ]
        # }
        result = []
        markets = self.safe_value(response, 'data')
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'symbol')
            baseId = self.safe_string(market, 'base_coin')
            quoteId = self.safe_string(market, 'count_coin')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'amount_precision'),
                'price': self.safe_integer(market, 'price_precision'),
            }
            active = True
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
            }
            result.append(entry)
        return result

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0] * 1000,
            float(ohlcv[1]),
            float(ohlcv[3]),
            float(ohlcv[4]),
            float(ohlcv[2]),
            float(ohlcv[5]),
        ]

    async def fetch_ohlcv(self, symbol='BTC/USDT', timeframe='1m', params={}, since=None, limit=None):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
        }
        response = await self.publicGetOpenApiGetRecords(self.extend(request, params))
        # Exchange response
        # {
        #     'code': '0',
        #     'msg': 'suc',
        #     'data': [
        #                 [
        #                     1529387760,  #Time Stamp
        #                     7585.41,  #Opening Price
        #                     7585.41,  #Highest Price
        #                     7585.41,  #Lowest Price
        #                     7585.41,  #Closing Price
        #                     0.0       #Transaction Volume
        #                 ]
        #             ]
        # }
        return self.parse_ohlcvs(self.safe_value(response, 'data'), market, timeframe, since, limit)

    async def fetch_order_book(self, symbol='BTC/USDT', limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'type': 'step0',
        }
        response = await self.publicGetOpenApiMarketDept(self.extend(request, params))
        # Exchange response
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": {
        #         "tick": {
        #             "time": 1529408112000,  #Refresh time of depth
        #             "asks":  #Ask orders
        #             [
        #                 [
        #                     "6753.31",  #Price of Ask 1
        #                     0.00306    #Order Size of Ask 1
        #                 ],
        #                 [
        #                     "6754.78",  #Price of Ask 2
        #                     0.61112   #Order Size of Ask 2
        #                 ]
        #                 ...
        #             ],
        #             "bids":  #Ask orders
        #             [
        #                 [
        #                     "6732.02",  #Price of Bid 1
        #                     0.18444     #Order Size of Bid 1
        #                 ],
        #                 [
        #                     "6730.08",  #Price of Bid 2
        #                     0.14662    #Order Size of Bid 2
        #                 ]
        #                 ...
        #             ]
        #         }
        data = self.safe_value(response, 'data')
        detailData = self.safe_value(data, 'tick')
        return self.parse_order_book(detailData, self.safe_value(detailData, 'time'))

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_integer(ticker, 'time')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetOpenApiGetTicker(self.extend(request))
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": {
        #         "high": 6796.63,
        #         "vol": 2364.85442742,
        #         "last": 6722.37,
        #         "low": 6399.28,
        #         "buy": "6721.56",
        #         "sell": "6747.47",
        #         "time": 1529406706715
        #     }
        # }
        result = self.safe_value(response, 'data')
        return self.parse_ticker(result, market)

    def parse_trade(self, trade, market=None):
        # Fetch My Trades Object
        #             {
        #                 "volume": "1.000",
        #                 "side": "BUY",
        #                 "price": "0.10000000",
        #                 "fee": "0.16431104",
        #                 "ctime": 1510996571195,
        #                 "deal_price": "0.10000000",
        #                 "id": 306,
        #                 "type": "买入"
        #             }
        # Fetch Trades Object
        #         {
        #             "amount": 0.99583,
        #             "trade_time": 1529408112000,
        #             "price": 6763.9,
        #             "id": 280101,
        #             "type": "sell"
        #         }
        timestamp = self.safe_string(trade, 'trade_time')
        if timestamp is None:
            timestamp = self.safe_string(trade, 'ctime')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        if amount is None:
            amount = self.safe_float(trade, 'volume')
        symbol = None
        if market is not None:
            symbol = self.safe_string(market, 'symbol')
        cost = None
        if price is not None:
            if amount is not None:
                cost = float(self.cost_to_precision(symbol, price * amount))
        tradeId = self.safe_string(trade, 'id')
        side = self.safe_string(trade, 'side')
        if side is None:
            side = self.safe_string(trade, 'type')
        feecost = self.safe_float(trade, 'fee')
        fee = None
        if feecost is not None:
            fee = {
                'cost': feecost,
                'currency': self.safe_string(trade, 'feeCoin'),
            }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': tradeId,
            'order': None,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_trades(self, symbol='BTC/USDT', params={}, since=None, limit=None):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetOpenApiGetTrades(self.extend(request, params))
        # Exchange response
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": [
        #         {
        #             "amount": 0.99583,
        #             "trade_time": 1529408112000,
        #             "price": 6763.9,
        #             "id": 280101,
        #             "type": "sell"
        #         }
        #     ]
        # }
        return self.parse_trades(self.safe_value(response, 'data'), market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params=None):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'time': str(self.milliseconds()),
            'symbol': market['id'],
            'side': side.upper(),
            'volume': amount,
        }
        if type == 'limit':
            request['type'] = '1'
            request['price'] = self.price_to_precision(symbol, price)
        else:
            request['type'] = '2'
            if side.upper() == 'BUY':
                currentSymbolDetail = await self.fetch_ticker(symbol)
                currentPrice = self.safe_float(currentSymbolDetail, 'last')
                if currentPrice is None:
                    raise InvalidOrder('Provide correct Symbol')
                request['volume'] = self.cost_to_precision(symbol, amount * currentPrice)
        response = await self.privatePostOpenApiCreateOrder(self.extend(request, params))
        # Exchange response
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": {
        #         "order_id": 34343
        #     }
        # }
        code = self.safe_string(response, 'code')
        if code != '0':
            raise InvalidOrder(response['msg'] + ' ' + self.json(response))
        result = self.safe_value(response, 'data')
        return await self.fetch_order(self.safe_string(result, 'order_id'), symbol)

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' CancelOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
            'time': self.milliseconds(),
        }
        response = await self.privatePostOpenApiCancelOrder(self.extend(request, params))
        # Exchange response
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": {}
        # }
        code = self.safe_string(response, 'code')
        if code != '0':
            raise InvalidOrder(response['msg'] + ' ' + self.json(response))
        return await self.fetch_order(id, symbol)

    async def fetch_my_trades(self, symbol=None, since=None, limit=100, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'time': self.milliseconds(),
            'page': 1,
            'pageSize': limit,
        }
        response = await self.privateGetOpenApiAllTrade(self.extend(request, params))
        # Exchange response
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": {
        #         "count": 22,
        #         "resultList": [
        #             {
        #                 "volume": "1.000",
        #                 "side": "BUY",
        #                 "price": "0.10000000",
        #                 "fee": "0.16431104",
        #                 "ctime": 1510996571195,
        #                 "deal_price": "0.10000000",
        #                 "id": 306,
        #                 "type": "买入"
        #             }
        #         ]
        #     }
        # }
        result = self.safe_value(response, 'data')
        return self.parse_trades(self.safe_value(result, 'resultList'), market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            '0': 'Historical Order Unsuccessful',
            '1': 'Open',
            '2': 'Closed',
            '3': 'Open',
            '4': 'Cancelled',
            '5': 'Cancelling',
            '6': 'Abnormal Orders',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbol = None
        baseId = self.safe_string(order, 'baseCoin')
        quoteId = self.safe_string(order, 'countCoin')
        base = self.safe_currency_code(baseId)  # unified
        quote = self.safe_currency_code(quoteId)
        if base is not None:
            if quote is not None:
                symbol = base + '/' + quote
        timestamp = self.safe_string(order, 'created_at')
        price = self.safe_float(order, 'price')
        filled = self.safe_float(order, 'deal_volume')
        remaining = self.safe_float(order, 'remain_volume')
        amount = self.safe_float(order, 'volume')
        id = self.safe_string(order, 'order_id')
        if id is None:
            id = self.safe_string(order, 'id')
        side = self.safe_string(order, 'side')
        cost = None
        type = None
        if filled is not None:
            if price is not None:
                cost = filled * price
        typeId = self.safe_integer(order, 'type')
        if typeId is not None:
            if typeId == 1:
                type = 'limit'
            else:
                type = 'market'
        trades = self.safe_value(order, 'tradeList')
        fee = None
        average = self.safe_float(order, 'avg_price')
        if trades is not None:
            trades = self.parse_trades(trades, market)
            feeCost = None
            numTrades = len(trades)
            for i in range(0, numTrades):
                if feeCost is None:
                    feeCost = 0
                tradeFee = self.safe_float(trades[i], 'fee')
                if tradeFee is not None:
                    feeCost = self.sum(feeCost, tradeFee)
            feeCurrency = None
            if market is not None:
                feeCurrency = market['quote']
            if feeCost is not None:
                fee = {
                    'cost': feeCost,
                    'currency': feeCurrency,
                }
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        }

    async def fetch_common_orders(self, symbol, limit, params):
        request = {
            'symbol': symbol,
            'time': self.milliseconds(),
            'page': 1,
            'pageSize': limit,
        }
        return await self.privateGetOpenApiNewOrder(self.extend(request, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=100, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' FetchOpenOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        response = await self.fetch_common_orders(market['id'], limit, params)
        result = self.safe_value(response, 'data')
        closedOrdered = self.filter_by(self.safe_value(result, 'resultList', {}), 'status', 2)
        return self.parse_orders(closedOrdered, market, since, limit)

    async def fetch_open_orders(self, symbol='None', since=None, limit=100, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' FetchOpenOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        response = await self.fetch_common_orders(market['id'], limit, params)
        # Exchange response
        # {
        #     "code": "0",
        #     "msg": "suc",
        #     "data": {
        #         "count": 10,
        #         "resultList": [
        #             {
        #                 "side": "BUY",
        #                 "total_price": "0.10000000",
        #                 "created_at": 1510993841000,
        #                 "avg_price": "0.10000000",
        #                 "countCoin": "btc",
        #                 "source": 1,
        #                 "type": 1,
        #                 "side_msg": "买入",
        #                 "volume": "1.000",
        #                 "price": "0.10000000",
        #                 "source_msg": "WEB",
        #                 "status_msg": "部分成交",
        #                 "deal_volume": "0.50000000",
        #                 "id": 424,
        #                 "remain_volume": "0.00000000",
        #                 "baseCoin": "eth",
        #                 "tradeList": [
        #                     {
        #                         "volume": "0.500",
        #                         "price": "0.10000000",
        #                         "fee": "0.16431104",
        #                         "ctime": 1510996571195,
        #                         "deal_price": "0.10000000",
        #                         "id": 306,
        #                         "type": "买入"
        #                     }
        #                 ],
        #                 "status": 3
        #             },
        #             {
        #                 "side": "SELL",
        #                 "total_price": "0.10000000",
        #                 "created_at": 1510993841000,
        #                 "avg_price": "0.10000000",
        #                 "countCoin": "btc",
        #                 "source": 1,
        #                 "type": 1,
        #                 "side_msg": "买入",
        #                 "volume": "1.000",
        #                 "price": "0.10000000",
        #                 "source_msg": "WEB",
        #                 "status_msg": "未成交",
        #                 "deal_volume": "0.00000000",
        #                 "id": 425,
        #                 "remain_volume": "0.00000000",
        #                 "baseCoin": "eth",
        #                 "tradeList": [],
        #                 "status": 1
        #             }
        #         ]
        #     }
        # }
        result = self.safe_value(response, 'data')
        ordered = self.filter_by(self.safe_value(result, 'resultList', {}), 'status', 1)
        partialOrdered = self.filter_by(self.safe_value(result, 'resultList', {}), 'status', 3)
        allOrders = self.array_concat(ordered, partialOrdered)
        return self.parse_orders(allOrders, market, since, limit)

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' FetchOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'time': (self.milliseconds()),
            'order_id': id,
        }
        response = await self.privateGetOpenApiOrderInfo(self.extend(request, params))
        result = self.safe_value(response, 'data')
        return self.parse_order(self.safe_value(result, 'order_info', {}))

    async def fetch_balance(self, params={}):
        await self.load_markets()
        request = {
            'time': self.milliseconds(),
        }
        response = await self.privateGetOpenApiUserAccount(self.extend(request, params))
        result = {'info': response}
        resultData = self.safe_value(response, 'data')
        balances = self.safe_value(resultData, 'coin_list')
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'coin')
            code = self.safe_currency_code(currencyId)
            account = {
                'free': self.safe_float(balance, 'normal'),
                'used': self.safe_float(balance, 'locked'),
                # 'total': self.safe_float(balance, 'balance'),
            }
            result[code] = account
        return self.parse_balance(result)

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        # EndPoints Result common pattern
        # {
        #     "code" : "code_id",
        #     "msg" : "",
        #     "data" : {}
        # }
        errorCode = self.safe_string(response, 'code')
        if errorCode == '0':
            # success
            return
        errorMessages = self.errorMessages
        message = None
        message = self.safe_string(response, 'msg')
        if message is None:
            message = self.safe_string(errorMessages, errorCode, 'Unknown Error')
        feedback = self.id + ' ' + message
        self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
        raise ExchangeError(feedback)
