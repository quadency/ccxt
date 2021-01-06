# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import CancelPending


class aax(Exchange):

    def describe(self):
        return self.deep_extend(super(aax, self).describe(), {
            'id': 'aax',
            'name': 'aax',
            'rateLimit': 500,
            'has': {
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOrderBook': True,
                'fetchTrades': True,
                'fetchBalance': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrders': True,
                'fetchOrder': True,
                'fetchTicker': True,
            },
            'timeframes': {
                '1m': 1,
                '3m': 3,
                '5m': 5,
                '15m': 15,
                '30m': 30,
                '1h': 60,
                '2h': 120,
                '3h': 180,
                '4h': 240,
                '8h': 480,
                '1d': 1440,
            },
            'headers': {
                'Content-Type': 'application/json',
            },
            'urls': {
                'api': 'https://api.aax.com',
                'www': 'https://www.aax.com/',
            },
            'api': {
                'public': {
                    'get': [
                        'v2/instruments',
                        'v2/market/orderbook',
                        'marketdata/v1/getHistMarketData',
                        'v2/market/trades',
                        'v2/market/tickers',
                    ],
                },
                'private': {
                    'get': [
                        'v2/account/balances',
                        'v2/spot/trades',
                        'v2/spot/openOrders',
                        'v2/spot/orders',
                        'v2/user/info',
                    ],
                    'post': [
                        'v2/spot/orders',
                    ],
                    'delete': [
                        'v2/spot/orders/cancel/{orderID}',
                    ],
                },
            },
            'exceptions': {
                '400': BadRequest,
                '401': AuthenticationError,
                '403': AuthenticationError,
                '429': PermissionDenied,
                '10003': BadRequest,
                '10006': AuthenticationError,
                '20001': InsufficientFunds,
                '20009': BadRequest,
                '30004': BadRequest,
                '30005': BadRequest,
                '30006': BadRequest,
                '30007': BadRequest,
                '30008': BadRequest,
                '30009': BadRequest,
                '30011': CancelPending,
                '30012': BadSymbol,
                '30013': BadSymbol,
                '30018': InvalidOrder,
                '30019': InvalidOrder,
                '30020': InvalidOrder,
                '30023': InvalidOrder,
                '30026': InvalidOrder,
                '30027': ExchangeError,
                '30030': InvalidOrder,
                '30047': InvalidOrder,
            },
            'errorMessages': {
                '400': 'There is something wrong with your request',
                '401': 'Your API key is wrong',
                '403': 'Your API key does not have enough privileges to access self resource',
                '429': 'You have exceeded your API key rate limits',
                '500': 'Internal Server Error',
                '503': 'Service is down for maintenance',
                '504': 'Request timeout expired',
                '550': 'You requested data that are not available at self moment',
                '10003': 'Parameter validation error',
                '10006': 'Session expired, please relogin',
                '20001': 'Insufficient balance. Please deposit to trade',
                '20009': 'Order amount must be positive',
                '30004': 'Minimum quantity is {0}',
                '30005': 'Quantity maximum precision is {0} decimal places',
                '30006': 'Price maximum precision is {0} decimal places',
                '30007': 'Minimum price is {0}',
                '30008': 'Stop price maximum precision is {0} decimal places',
                '30009': 'Stop Price cannot be less than {0}',
                '30011': 'The order is being cancelled, please wait',
                '30012': 'Unknown currency',
                '30013': 'Unknown symbol',
                '30018': 'Order price cannot be greater than {0}',
                '30019': 'Order quantity cannot be greater than {0}',
                '30020': 'Order price must be a multiple of {0}',
                '30023': 'Order failed, please try again',
                '30026': 'Quantity is not a multiple of {0}',
                '30027': 'Close position failed, it is recommended that you cancel the current order and then close the position',
                '30028': 'Symbol cannot be traded at self time',
                '30030': 'Price cannot be specified for market orders',
                '30037': 'Once stop limit order triggered, stop price cannot be amended',
                '30040': 'Order status has changed, please try again later',
                '30047': 'The order is closed. Can nott cancel',
                '30049': 'The order is being modified, please wait',
                '40009': 'Too many requests',
                '50001': 'Server side exception, please try again later',
                '50002': 'Server is busy, please try again later',
            },
        })

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api']
        queryParams = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public' or method == 'GET':
            if query:
                queryParams += '?' + self.urlencode(query)
        if api == 'private':
            nonce = str(self.milliseconds())
            signature = nonce + ':' + method + queryParams
            if method != 'GET' and method != 'HEAD':
                body = self.json(query)
                signature += body
            encodedHEX = self.hmac(self.encode(signature), self.encode(self.secret), hashlib.sha256)
            headers = {
                'X-ACCESS-KEY': self.apiKey,
                'X-ACCESS-NONCE': nonce,
                'X-ACCESS-SIGN': encodedHEX,
            }
        url += queryParams
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def fetch_markets(self, params={}):
        response = await self.publicGetV2Instruments()
        # Exchange Response
        # {
        #     "code":1,
        #     "data":[
        #        {
        #           "tickSize":"0.1",
        #           "lotSize":"0.0001",
        #           "base":"BTC",
        #           "quote":"USDT",
        #           "minQuantity":"0.0010000000",
        #           "maxQuantity":"999900.0000000000",
        #           "minPrice":"0.1000000000",
        #           "maxPrice":"10000000.0000000000",
        #           "status":"enable",
        #           "symbol":"BTCUSDT",
        #           "code":null,
        #           "takerFee":"0.00000",
        #           "makerFee":"0.00000",
        #           "multiplier":"1.000000000000",
        #           "mmRate":"0.02500",
        #           "imRate":"0.05000",
        #           "type":"spot"
        #        },
        #        ...
        #     ],
        #     "message":"success",
        #     "ts":1573561743499
        #  }
        result = []
        markets = self.safe_value(response, 'data')
        for i in range(0, len(markets)):
            market = markets[i]
            code = self.safe_string(market, 'code')
            if (code and code.upper() == 'FP'):
                continue
            id = self.safe_string(market, 'symbol')
            baseId = self.safe_string(market, 'base')
            quoteId = self.safe_string(market, 'quote')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = baseId + '/' + quoteId
            status = self.safe_string(market, 'status')
            active = None
            if status is not None:
                active = (status.upper() == 'ENABLE')
            precision = {
                'price': self.precision_from_string(market['tickSize']),
                'amount': self.precision_from_string(market['lotSize']),
            }
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
                'type': self.safe_string(market, 'type'),
                'taker': self.safe_float(market, 'takerFee'),
                'maker': self.safe_float(market, 'makerFee'),
                'limits': {
                    'amount': {
                        'min': self.safe_float(market, 'minQuantity'),
                        'max': self.safe_float(market, 'maxQuantity'),
                    },
                    'price': {
                        'min': self.safe_float(market, 'minPrice'),
                        'max': self.safe_float(market, 'maxPrice'),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
            }
            result.append(entry)
        return result

    async def fetch_ohlcv(self, symbol='BTC/USDT', timeframe='1m', since=None, limit=30, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'date_scale': self.timeframes[timeframe],
            'base': market['base'],
            'quote': market['quote'],
            'limit': limit,
        }
        if since is not None:
            request['from'] = since
        if 'to' in params:
            request['to'] = params['to']
        response = await self.publicGetMarketdataV1GetHistMarketData(self.extend(request, params))
        result = []
        if 's' in response and response['s'] == 'ok':
            timeArr = response['t']
            openArr = response['o']
            highArr = response['h']
            lowArr = response['l']
            closeArr = response['c']
            volumeArr = response['v']
            prevOpenTime = None
            for i in range(0, len(timeArr)):
                openTime = (int(timeArr[i]) * 1000)
                if openTime != prevOpenTime:
                    ohlcvArr = []
                    ohlcvArr.append(openTime)
                    ohlcvArr.append(openArr[i])
                    ohlcvArr.append(highArr[i])
                    ohlcvArr.append(lowArr[i])
                    ohlcvArr.append(closeArr[i])
                    ohlcvArr.append(volumeArr[i] / closeArr[i])
                    result.append(ohlcvArr)
                    prevOpenTime = openTime
        return self.parse_ohlcvs(result, market, timeframe, since, limit)

    def parse_ticker(self, ticker, market=None, time=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = time
        open = self.safe_float(ticker, 'o')
        last = self.safe_float(ticker, 'c')
        change = None
        percentage = None
        average = None
        if last is not None and open is not None:
            change = last - open
            average = self.sum(last, open) / 2
            if open > 0:
                percentage = change / open * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'h'),
            'low': self.safe_float(ticker, 'l'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, 'v'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetV2MarketTickers(self.extend(params))
        result = self.safe_value(response, 'tickers', [])
        pair = market['id']
        for i in range(0, len(result)):
            ticker = result[i]
            if pair == ticker['s']:
                return self.parse_ticker(ticker, market, self.safe_integer(response, 't'))
        return None

    async def fetch_order_book(self, symbol='BTC/USDT', limit=50, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'level': limit,
        }
        response = await self.publicGetV2MarketOrderbook(self.extend(request, params))
        # Response Format
        # {
        #     "asks":[
        #        [
        #           "10823.00000000",  #price
        #           "0.004000"  #size
        #        ],
        #        [
        #           "10823.10000000",
        #           "0.100000"
        #        ],
        #        [
        #           "10823.20000000",
        #           "0.010000"
        #        ]
        #     ],
        #     "bids":[
        #        [
        #           "10821.20000000",
        #           "0.002000"
        #        ],
        #        [
        #           "10821.10000000",
        #           "0.005000"
        #        ],
        #        [
        #           "10820.40000000",
        #           "0.013000"
        #        ]
        #     ],
        #     "e":"BTCUSDT@book_50",
        #     "t":1561543614756
        #  }
        timestamp = self.safe_integer(response, str('t'))
        return self.parse_order_book(response, timestamp)

    def parse_trade(self, trade, market=None):
        # From FetchTrades
        #   {
        #     "e":"BTCUSDFP@trades",
        #     "trades":
        #         [{"p":"9395.50000000",
        #            "q":"50.000000",
        #            "t":1592563996718
        #          },
        #         { "p":"9395.50000000",
        #            "q":"50.000000",
        #            "t":1592563993577
        #         }]
        #   }
        # Response From FetchMyTrdaes
        # {
        #        [
        #           {
        #              "avgPrice":"8000",
        #              "base":"BTC",
        #              "commission":"0.00000888",
        #              "createTime":"2019-11-12T03:18:35Z",
        #              "cumQty":"0.0148",
        #              "filledPrice":"8000",
        #              "filledQty":"0.0148",
        #              "leavesQty":"0.0052",
        #              "orderID":"wFo9ZPxAJ",
        #              "orderQty":"0.02",
        #              "orderStatus":2,
        #              "orderType":2,
        #              "price":"8000",
        #              "quote":"USDT",
        #              "rejectCode":0,
        #              "rejectReason":null,
        #              "side":1,
        #              "stopPrice":"0",
        #              "symbol":"BTCUSDT",
        #              "taker":false,
        #              "transactTime":"2019-11-12T03:16:16Z",
        #              "updateTime":null,
        #              "userID":"216214"
        #           }
        #        ],
        #  }
        timestamp = self.safe_string(trade, 't')
        if timestamp is None:
            timestamp = self.safe_string(trade, 'createTime')
            if timestamp is not None:
                timestamp = self.parse8601(timestamp)
        symbol = None
        if market is not None:
            symbol = self.safe_string(market, 'symbol')
        if symbol is None:
            base = self.safe_string(trade, 'base')
            quote = self.safe_string(trade, 'quote')
            if base is not None and quote is not None:
                symbol = base + '/' + quote
        price = self.safe_float_2(trade, 'p', 'avgPrice')
        amount = self.safe_float_2(trade, 'q', 'orderQty')
        sideType = self.safe_integer(trade, 'side')
        side = None
        if sideType is not None:
            if sideType == 1:
                side = 'BUY'
            if sideType == 2:
                side = 'SELL'
        if side is None:
            if price < 0:
                side = 'SELL'
            else:
                side = 'BUY'
            price = abs(price)
        cost = None
        if price is not None and amount is not None and symbol is not None:
            cost = float(self.cost_to_precision(symbol, price * amount))
        takerOrMaker = None
        if 'taker' in trade:
            takerOrMaker = 'taker' if trade['taker'] else 'maker'
        orderId = self.safe_string(trade, 'orderID')
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': orderId,
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': self.safe_string(trade, 'commission'),
        }

    async def fetch_trades(self, symbol, since=None, limit=2000, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'limit': limit,
        }
        response = await self.publicGetV2MarketTrades(self.extend(request, params))
        # Response Received
        # {
        #     "e":"BTCUSDFP@trades",
        #     "trades":
        #         [{"p":"9395.50000000",
        #            "q":"50.000000",
        #            "t":1592563996718
        #          },
        #         { "p":"9395.50000000",
        #            "q":"50.000000",
        #            "t":1592563993577
        #         }]
        #   }
        return self.parse_trades(self.safe_value(response, 'trades'), market, since, limit)

    async def fetch_balance(self, params={}):
        request = {
            'purseType': 'SPTP',  # spot only for now
        }
        response = await self.privateGetV2AccountBalances(self.extend(request, params))
        # FetchBalance Response
        #    {
        #      "code":1,
        #      "data":[
        #      {
        #        "purseType":"FUTP",
        #        "currency":"BTC",
        #        "available":"0.41000000",
        #        "unavailable":"0.00000000"
        #      },
        #      {
        #        "purseType":"FUTP",
        #        "currency":"USDT",
        #        "available":"0.21000000",
        #        "unvaliable":"0.00000000"
        #      }
        #    ]
        #      "message":"success",
        #      "ts":1573530401020
        #    }
        result = {'info': response}
        balances = self.safe_value(response, 'data')
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = {
                'free': self.safe_float(balance, 'available'),
                'used': self.safe_float(balance, 'unavailable'),
            }
            result[code] = account
        return self.parse_balance(result)

    def parse_order_type(self, type):
        orderTypes = {
            '1': 'market',
            '2': 'limit',
            '3': 'stop',
            '4': 'stop-limit',
        }
        return self.safe_string(orderTypes, type, type)

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',  # pending-new
            '1': 'open',  # new
            '2': 'open',  # partiallyfilled
            '3': 'closed',  # filled
            '4': 'canceled',  # cancel - rejected
            '5': 'canceled',  # canceled
            '6': 'rejected',  # rejected
            '10': 'canceled',  # canceled
            '11': 'rejected',  # business-rejct
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None, time=None):
        # CraeteOrder,cancelOrder Response
        #       {
        #        "avgPrice":"0",
        #        "base":"BTC",
        #        "clOrdID":"aax",
        #        "commission":"0",
        #        "createTime":null,
        #        "cumQty":"0",
        #        "id":null,
        #        "isTriggered":null,
        #        "lastPrice":"0",
        #        "lastQty":"0",
        #        "leavesQty":"0",
        #        "orderID":"wJ4L366KB",
        #        "orderQty":"0.02",
        #        "orderStatus":0,
        #        "orderType":2,
        #        "price":"8000",
        #        "quote":"USDT",
        #        "rejectCode":null,
        #        "rejectReason":null,
        #        "side":1,
        #        "stopPrice":null,
        #        "symbol":"BTCUSDT",
        #        "transactTime":null,
        #        "updateTime":null,
        #        "timeInForce":1,
        #        "userID":"216214"
        #     },
        timestamp = self.safe_string(order, 'createTime')
        if timestamp is None and time is not None:
            timestamp = time
        else:
            if len(timestamp) != 13:
                timestamp = self.parse8601(timestamp)
            else:
                timestamp = int(timestamp)
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'orderQty')
        cost = None
        symbol = None
        if market is not None:
            symbol = self.safe_string(market, 'symbol')
        if symbol is None:
            base = self.safe_string(order, 'base')
            quote = self.safe_string(order, 'quote')
            if base is not None and quote is not None:
                symbol = base + '/' + quote
        if price is not None and amount is not None and symbol is not None:
            cost = float(self.cost_to_precision(symbol, price * amount))
        sideType = self.safe_integer(order, 'side')
        side = None
        if sideType is not None:
            if sideType == 1:
                side = 'BUY'
            if sideType == 2:
                side = 'SELL'
        remaining = self.safe_float(order, 'leavesQty')
        filled = None
        if remaining is not None and amount is not None:
            filled = amount - remaining
        orderType = self.parse_order_type(self.safe_string(order, 'orderType'))
        status = self.parse_order_status(self.safe_string(order, 'orderStatus'))
        return {
            'info': order,
            'id': self.safe_string(order, 'orderID'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': orderType,
            'side': side,
            'price': price,
            'stop_price': self.safe_string(order, 'stopPrice'),
            'amount': amount,
            'cost': cost,
            'average': self.safe_float(order, 'avgPrice'),
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': self.safe_string(order, 'commission'),
            'trades': None,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        type = type.upper()
        if type == 'STOP_LIMIT':
            type = 'STOP-LIMIT'
        request = {
            # == Required ==
            # orderType : string  # can be MARKET,LIMIT,STOP,STOP-LIMIT
            # symbol : string
            # orderQty : string  # Buying or selling quantity
            # side : string  # BUY or SELL
            # == Required according to ordeType ==
            # price : string  # limit price in limit and stop-limit orders
            # stopPrice : string  # Trigger price for stop-limit order and stop order
            # == Optional ==
            # clOrdID : string
            # timeInForce :string  # GTC/IOC/FOK，default is GTC
            'orderType': type,
            'symbol': market['id'],
            'orderQty': self.amount_to_precision(symbol, amount),
            'side': side.upper(),
        }
        if (type == 'LIMIT') or (type == 'STOP-LIMIT'):
            if price is None:
                raise InvalidOrder(self.id + ' createOrder method requires a price for a ' + type + ' order')
            request['price'] = self.price_to_precision(symbol, price)
        if (type == 'STOP') or (type == 'STOP-LIMIT'):
            stopPrice = self.safe_float(params, 'stopPrice')
            if stopPrice is None:
                raise InvalidOrder(self.id + ' createOrder method requires a stopPrice extra param for a ' + type + ' order')
            request['stopPrice'] = self.price_to_precision(symbol, stopPrice)
        response = await self.privatePostV2SpotOrders(self.extend(request, params))
        # Response
        # {
        #     "code":1,
        #     "data":{
        #        "avgPrice":"0",
        #        "base":"BTC",
        #        "clOrdID":"aax",
        #        "commission":"0",
        #        "createTime":null,
        #        "cumQty":"0",
        #        "id":null,
        #        "isTriggered":null,
        #        "lastPrice":"0",
        #        "lastQty":"0",
        #        "leavesQty":"0",
        #        "orderID":"wJ4L366KB",
        #        "orderQty":"0.02",
        #        "orderStatus":0,
        #        "orderType":2,
        #        "price":"8000",
        #        "quote":"USDT",
        #        "rejectCode":null,
        #        "rejectReason":null,
        #        "side":1,
        #        "stopPrice":null,
        #        "symbol":"BTCUSDT",
        #        "transactTime":null,
        #        "updateTime":null,
        #        "timeInForce":1,
        #        "userID":"216214"
        #     },
        #     "message":"success",
        #     "ts":1573530401264
        #  }
        return self.parse_order(self.safe_value(response, 'data'), market, self.safe_string(response, 'ts'))

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            await self.load_markets()
            market = self.market(symbol)
        request = {
            'orderID': id,
        }
        response = await self.privateDeleteV2SpotOrdersCancelOrderID(self.extend(request, params))
        # Response
        # {
        #     "code":1,
        #     "data":{
        #        "avgPrice":"0",
        #        "base":"BTC",
        #        "clOrdID":"aax",
        #        "commission":"0",
        #        "createTime":"2019-11-12T03:46:41Z",
        #        "cumQty":"0",
        #        "id":"114330021504606208",
        #        "isTriggered":false,
        #        "lastPrice":"0",
        #        "lastQty":"0",
        #        "leavesQty":"0",
        #        "orderID":"wJ4L366KB",
        #        "orderQty":"0.05",
        #        "orderStatus":1,
        #        "orderType":2,
        #        "price":"8000",
        #        "quote":"USDT",
        #        "rejectCode":0,
        #        "rejectReason":null,
        #        "side":1,
        #        "stopPrice":"0",
        #        "symbol":"BTCUSDT",
        #        "transactTime":null,
        #        "updateTime":"2019-11-12T03:46:41Z",
        #        "timeInForce":1,
        #        "userID":"216214"
        #     },
        #     "message":"success",
        #     "ts":1573530402029
        #  }
        return self.parse_order(self.safe_value(response, 'data'), market, self.safe_string(response, 'ts'))

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            # pageNum : Integer  # optional
            # pageSize : Integer  # optional
            # base : String  # optional
            # quote : String  # optional
            # orderId : String  #optional
            # startDate : String  #optional
            # endDate : String  #optional
            # side : String  # optional
            # orderType : String  # optional
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['base'] = market['baseId']
            request['quote'] = market['quoteId']
        if since is not None:
            request['startDate'] = self.ymd(since, '-')
        if limit is not None:
            request['pageSize'] = limit
        response = await self.privateGetV2SpotTrades(self.extend(request, params))
        # Response
        # {
        #     "code":1,
        #     "data":{
        #        "list":[
        #           {
        #              "avgPrice":"8000",
        #              "base":"BTC",
        #              "commission":"0.00000888",
        #              "createTime":"2019-11-12T03:18:35Z",
        #              "cumQty":"0.0148",
        #              "filledPrice":"8000",
        #              "filledQty":"0.0148",
        #              "id":"114322949580906499",
        #              "leavesQty":"0.0052",
        #              "orderID":"wFo9ZPxAJ",
        #              "orderQty":"0.02",
        #              "orderStatus":2,
        #              "orderType":2,
        #              "price":"8000",
        #              "quote":"USDT",
        #              "rejectCode":0,
        #              "rejectReason":null,
        #              "side":1,
        #              "stopPrice":"0",
        #              "symbol":"BTCUSDT",
        #              "taker":false,
        #              "transactTime":"2019-11-12T03:16:16Z",
        #              "updateTime":null,
        #              "userID":"216214"
        #           }
        #        ],
        #        "pageNum":1,
        #        "pageSize":1,
        #        "total":10
        #     },
        #     "message":"success",
        #     "ts":1573532934832
        #  }
        result = self.safe_value(response, 'data')
        return self.parse_trades(self.safe_value(result, 'list', []), market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            # pageNum : Integer  # optional
            # pageSize : Integer  # optional
            # symbol : String  # optional
            # orderId : String  # optional
            # side : String  # optional
            # orderType : String  # optional
            # clOrdID : String  #optional
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if limit is not None:
            request['pageSize'] = limit
        response = await self.privateGetV2SpotOpenOrders(self.extend(request, params))
        # Response
        # {
        #     "code":1,
        #     "data":{
        #        "list":[
        #           {
        #              "avgPrice":"0",
        #              "base":"BTC",
        #              "clOrdID":"aax",
        #              "commission":"0",
        #              "createTime":"2019-11-12T03:41:52Z",
        #              "cumQty":"0",
        #              "id":"114328808516083712",
        #              "isTriggered":false,
        #              "lastPrice":"0",
        #              "lastQty":"0",
        #              "leavesQty":"0",
        #              "orderID":"wJ3qitASB",
        #              "orderQty":"0.02",
        #              "orderStatus":1,
        #              "orderType":2,
        #              "price":"8000",
        #              "quote":"USDT",
        #              "rejectCode":0,
        #              "rejectReason":null,
        #              "side":1,
        #              "stopPrice":"0",
        #              "symbol":"BTCUSDT",
        #              "transactTime":null,
        #              "updateTime":"2019-11-12T03:41:52Z",
        #              "timeInForce":1,
        #              "userID":"216214"
        #           },
        #           ...
        #        ],
        #        "pageNum":1,
        #        "pageSize":2,
        #        "total":2
        #     },
        #     "message":"success",
        #     "ts":1573553718212
        #  }
        result = self.safe_value(response, 'data')
        return self.parse_orders(self.safe_value(result, 'list', []), market, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=100, params={}):
        await self.load_markets()
        request = {
            # pageNum : Integer  # optional
            # pageSize : Integer  # optional
            # symbol : String  # optional
            # orderId : String  # optional
            # side : String  # optional
            # orderType : String  # optional
            # clOrdID : String  #optional
            # base : string  # optional
            # quote :string  # optional
            # orderStatus : Integer  #optional 1: new, 2:filled, 3:cancel
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['base'] = market['baseId']
            request['quote'] = market['quoteId']
        if limit is not None:
            request['pageSize'] = limit
        response = await self.privateGetV2SpotOrders(self.extend(request, params))
        result = self.safe_value(response, 'data')
        return self.parse_orders(self.safe_value(result, 'list', []), market, since, limit)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'orderID': id,
        }
        response = await self.privateGetV2SpotOrders(self.extend(request, params))
        result = self.safe_value(response, 'data')
        list = self.safe_value(result, 'list', [])
        return self.parse_order(list[0])

    async def fetch_user_id(self):
        response = await self.privateGetV2UserInfo()
        result = self.safe_value(response, 'data')
        return self.safe_value(result, 'userID')

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        errorCode = self.safe_string(response, 'code')
        if errorCode is None:
            # fetchOrderBook or fetchTrades or fetchOhlcv
            return
        if errorCode == '1':
            # success
            return
        errorMessages = self.errorMessages
        message = None
        message = self.safe_string(response, 'message')
        if message is None:
            message = self.safe_string(errorMessages, errorCode, 'Unknown Error')
        feedback = self.id + ' ' + message
        self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
        raise ExchangeError(feedback)
