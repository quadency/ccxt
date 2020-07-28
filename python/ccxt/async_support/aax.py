# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange


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
                    ],
                },
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
            },
        })

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api']
        url += '/' + path
        query = self.omit(params, self.extract_params(path))
        if query:
            url += '?' + self.urlencode(query)
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
                active = (status.upper() == 'ENABLE' or status.upper() == 'READONLY')
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
            for i in range(0, len(timeArr)):
                ohlcvArr = []
                ohlcvArr.append(int(timeArr[i]) * 1000)
                ohlcvArr.append(openArr[i])
                ohlcvArr.append(highArr[i])
                ohlcvArr.append(lowArr[i])
                ohlcvArr.append(closeArr[i])
                ohlcvArr.append(volumeArr[i])
                result.append(ohlcvArr)
        return self.parse_ohlcvs(result, market, timeframe, since, limit)

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
        timestamp = self.safe_integer(trade, str('t'))
        symbol = None
        if market is not None:
            symbol = self.safe_string(market, 'symbol')
        price = self.safe_float(trade, 'p')
        amount = self.safe_float(trade, 'q')
        side = 'BUY'
        cost = None
        if price is not None:
            if price < 0:
                side = 'SELL'
            price = abs(price)
            if amount is not None:
                if symbol is not None:
                    cost = float(self.cost_to_precision(symbol, price * amount))
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': None,
            'order': None,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
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
