'use strict';

//  ---------------------------------------------------------------------------

const Exchange = require ('./base/Exchange');
// const { ExchangeError } = require ('./base/errors');
const { TRUNCATE, DECIMAL_PLACES } = require ('./base/functions/number');

//  ---------------------------------------------------------------------------

module.exports = class kryptono extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'kryptono',
            'name': 'Kryptono',
            'countries': ['SG'],
            'version': 'v2',
            'rateLimit': 1000, // TODO: Check if this is the corrrect as per CCXT requirments. Kryptono gives 1000 minute intervals.
            'certified': true, // TODO: Verify with Tony.
            // new metainfo interface
            'has': {
                'CORS': true,
                'fetchMarkets': true,
                'fetchCurrencies': true,
                'fetchTradingLimits': false,
                'fetchFundingLimits': false,
                'fetchTickers': true, // TODO : Check with doc for fetchTicker
                'fetchOrderBook': true,
                'fetchTrades': true,
                'fetchOHLCV': true,
                'fetchBalance': true,
                'fetchTransactions': false,
                'withdraw': false,
                'desposit': false,
                'fetchDeposits': false,
                'fetchWithdrawals': false,
                'fetchDepositAddress': false,
                'fetchOrder': true, // todo /api/v2/order/details
                'fetchOrders': true, // todo  /api/v2/order/list/completed
                'fetchOpenOrders': true, // todo /api/v2/order/list/open
                'fetchClosedOrders': false, // todo api/v2/order/list/completed
                'fetchMyTrades': 'emulated', // todo /api/v2/order/list/trades
            },
            'timeframes': {
                // TODO: Check if all of these intervals are supported.
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
                        // these endpoints require this.apiKey + this.secret
                        'account/balances',
                        'account/details',
                        'order/list/all',
                        'order/list/open',
                        'order/list/completed',
                        'order/list/trades',
                        'order/trade-detail',
                    ],
                    'post': [
                        'order/test',
                        'order/details',
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
            'fees': {
                'trading': {
                    'tierBased': false,
                    'percentage': true,
                    'taker': 0.001,
                    'maker': 0.001,
                },
            },
            // todo Trading API Information in `https://kryptono.exchange/k/api#developers-guide-api-v2-for-kryptono-exchange-july-13-2018`
            'exceptions': {
                // 'Call to Cancel was throttled. Try again in 60 seconds.': DDoSProtection,
                // 'Call to GetBalances was throttled. Try again in 60 seconds.': DDoSProtection,
                // 'APISIGN_NOT_PROVIDED': AuthenticationError,
                // 'INVALID_SIGNATURE': AuthenticationError,
                // 'INVALID_CURRENCY': ExchangeError,
                // 'INVALID_PERMISSION': AuthenticationError,
                // 'INSUFFICIENT_FUNDS': InsufficientFunds,
                // 'QUANTITY_NOT_PROVIDED': InvalidOrder,
                // 'MIN_TRADE_REQUIREMENT_NOT_MET': InvalidOrder,
                // 'ORDER_NOT_OPEN': OrderNotFound,
                // 'INVALID_ORDER': InvalidOrder,
                // 'UUID_INVALID': OrderNotFound,
                // 'RATE_NOT_PROVIDED': InvalidOrder, // createLimitBuyOrder ('ETH/BTC', 1, 0)
                // 'WHITELIST_VIOLATION_IP': PermissionDenied,
                // 'DUST_TRADE_DISALLOWED_MIN_VALUE': InvalidOrder,
                // 'RESTRICTED_MARKET': BadSymbol,
                // 'We are down for scheduled maintenance, but we\u2019ll be back up shortly.': OnMaintenance, // {"success":false,"message":"We are down for scheduled maintenance, but we\u2019ll be back up shortly.","result":null,"explanation":null}
            },
            'options': {
                'parseOrderStatus': false,
                'hasAlreadyAuthenticatedSuccessfully': false, // a workaround for APIKEY_INVALID
                'symbolSeparator': '_',
                // With certain currencies, like
                // AEON, BTS, GXS, NXT, SBD, STEEM, STR, XEM, XLM, XMR, XRP
                // an additional tag / memo / payment id is usually required by exchanges.
                // With Bittrex some currencies imply the "base address + tag" logic.
                // The base address for depositing is stored on this.currencies[code]
                // The base address identifies the exchange as the recipient
                // while the tag identifies the user account within the exchange
                // and the tag is retrieved with fetchDepositAddress.
                'tag': {
                    'NXT': true, // NXT, BURST
                    'CRYPTO_NOTE_PAYMENTID': true, // AEON, XMR
                    'BITSHAREX': true, // BTS
                    'RIPPLE': true, // XRP
                    'NEM': true, // XEM
                    'STELLAR': true, // XLM
                    'STEEM': true, // SBD, GOLOS
                    // https://github.com/ccxt/ccxt/issues/4794
                    // 'LISK': true, // LSK
                },
                'subaccountId': undefined,
                // see the implementation of fetchClosedOrdersV3 below
                'fetchClosedOrdersMethod': 'fetch_closed_orders_v3',
                'fetchClosedOrdersFilterBySince': true,
            },
        });
    }

    costToPrecision (symbol, cost) {
        return this.decimalToPrecision (cost, TRUNCATE, this.markets[symbol]['precision']['price'], DECIMAL_PLACES);
    }

    feeToPrecision (symbol, fee) {
        return this.decimalToPrecision (fee, TRUNCATE, this.markets[symbol]['precision']['price'], DECIMAL_PLACES);
    }

    async fetchMarkets (params = {}) {
        const response = await this.v2GetExchangeInfo (params);
        const symbols = this.safeValue (response, 'symbols');
        // they mislabeled quotes to base
        const quotes = this.safeValue (response, 'base_currencies');
        const minQuotesMap = {};
        for (let i = 0; i < quotes.length; i++) {
            minQuotesMap[quotes[i]['currency_code']] = {
                'min': parseFloat (quotes[i]['minimum_total_order']),
            };
        }
        const base = this.safeValue (response, 'coins');
        const minBaseMap = {};
        for (let i = 0; i < base.length; i++) {
            minBaseMap[base[i]['currency_code']] = {
                'min': parseFloat (base[i]['minimum_order_amount']),
            };
        }
        const result = [];
        for (let i = 0; i < symbols.length; i++) {
            const [base, quote] = symbols[i]['symbol'].split (this.options['symbolSeparator']);
            const hasLimitMin = this.safeValue (minBaseMap, base);
            let limitAmountMin = 0;
            if (hasLimitMin) {
                limitAmountMin = hasLimitMin['min'];
            }
            const hasPriceMin = this.safeValue (minQuotesMap, quote);
            let priceAmountMin = 0;
            if (hasPriceMin) {
                priceAmountMin = hasPriceMin['min'];
            }
            result.push ({
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
                        'min': limitAmountMin,
                        'max': undefined,
                    },
                    'price': {
                        'min': priceAmountMin,
                        'max': undefined,
                    },
                },
            });
        }
        return result;
    }

    async fetchBalance (params = {}) {
        await this.loadMarkets ();
        const hasRecvWindow = this.safeValue (params, 'recvWindow');
        if (!hasRecvWindow) {
            params['recvWindow'] = 5000;
        }
        const response = await this.v2GetAccountBalances (params);
        const result = { 'info': response };
        for (let i = 0; i < response.length; i++) {
            result[response[i]['currency_code']] = {
                'free': response[i]['available'],
                'used': response[i]['in_order'],
                'total': response[i]['total'],
            };
        }
        return this.parseBalance (result);
    }

    parseOrderStatus (status) {
        const statuses = {
            'open': 'open',
            'partial_fill': 'open',
            'filled': 'closed',
            'canceled': 'canceled',
            'canceling': 'open',
        };
        return this.safeString (statuses, status, status);
    }

    parseOrder (order, market = undefined) {
        const timestamp = this.safeString (order, 'createTime');
        let symbol = undefined;
        const marketId = this.safeString (order, 'order_symbol');
        if (marketId !== undefined) {
            if (marketId in this.markets_by_id) {
                market = this.markets_by_id[marketId];
                symbol = market['symbol'];
            } else {
                const [ baseId, quoteId ] = marketId.split (this.options['symbolSeparator']);
                symbol = baseId + '/' + quoteId;
            }
        }
        const amount = this.safeFloat (order, 'order_size');
        const filled = this.safeFloat (order, 'executed');
        let remaining = undefined;
        if (amount !== undefined) {
            if (filled !== undefined) {
                remaining = amount - filled;
            }
        }
        return {
            'id': this.safeString (order, 'order_id'),
            'info': order,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'lastTradeTimestamp': undefined,
            'status': this.parseOrderStatus (this.safeString (order, 'status')),
            'symbol': symbol,
            'type': this.safeString (order, 'type'),
            'side': (this.safeString (order, 'order_side')).toLowerCase (),
            'price': this.safeFloat (order, 'order_price'),
            'cost': this.safeFloat (order, 'avg'),
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': undefined,
        };
    }

    async fetchOrder (id, symbol = undefined, params = {}) {
        await this.loadMarkets ();
        const request = {
            'order_id': id,
            'timestamp': this.milliseconds (),
        };
        const recvWindowParam = this.safeValue (params, 'recvWindow');
        let recvWindow = 5000;
        if (recvWindowParam) {
            recvWindow = recvWindowParam;
        }
        request['recvWindow'] = recvWindow;
        const response = await this.v2PostOrderDetails (this.extend (request, params));
        return this.parseOrder (response);
    }

    async fetchOrderBook (symbol, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const request = {
            'symbol': symbol.replace ('/', '_'),
        };
        const response = await this.v1GetDp (this.extend (request, params));
        //
        // {
        //     "symbol" : "KNOW_BTC",
        //     "limit" : 100,
        //     "asks" : [
        //       [
        //         "0.00001850",   // price
        //         "69.00000000"   // size
        //       ]
        //     ],
        //     "bids" : [
        //       [
        //         "0.00001651",       // price
        //         "11186.00000000"    // size
        //       ]
        //     ]
        //     "time" : 1529298130192
        //   }
        //
        return this.parseOrderBook (response, response['time']);
    }

    parseTicker (ticker, market = undefined) {
        //
        //     {
        //         "MarketName":"KNOW-BTC",
        //         "High":0.00001313,
        //         "Low":0.0000121,
        //         "BaseVolume":24.06681016,
        //         "Last":0.00001253,
        //         "TimeStamp":"2018-07-10T07:44:56.936Z",
        //         "Volume":1920735.0486831602,
        //         "Bid":"0.00001260",
        //         "Ask":"0.00001242",
        //         "PrevDay":0.00001253
        //       }
        //
        const timestamp = this.parse8601 (this.safeString (ticker, 'TimeStamp'));
        let symbol = undefined;
        const marketId = this.safeString (ticker, 'MarketName');
        if (marketId !== undefined) {
            if (marketId in this.markets_by_id) {
                market = this.markets_by_id[marketId];
            } else {
                symbol = this.parseSymbol (marketId);
            }
        }
        if ((symbol === undefined) && (market !== undefined)) {
            symbol = market['symbol'];
        }
        const previous = this.safeFloat (ticker, 'PrevDay');
        const last = this.safeFloat (ticker, 'Last');
        let change = undefined;
        let percentage = undefined;
        if (last !== undefined) {
            if (previous !== undefined) {
                change = last - previous;
                if (previous > 0) {
                    percentage = (change / previous) * 100;
                }
            }
        }
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'high': this.safeFloat (ticker, 'High'),
            'low': this.safeFloat (ticker, 'Low'),
            'bid': this.safeFloat (ticker, 'Bid'),
            'bidVolume': undefined,
            'ask': this.safeFloat (ticker, 'Ask'),
            'askVolume': undefined,
            'vwap': undefined,
            'open': previous,
            'close': last,
            'last': last,
            'previousClose': undefined,
            'change': change,
            'percentage': percentage,
            'average': undefined,
            'baseVolume': this.safeFloat (ticker, 'Volume'),
            'quoteVolume': this.safeFloat (ticker, 'BaseVolume'),
            'info': ticker,
        };
    }

    async fetchTickers (symbols = undefined, params = {}) {
        await this.loadMarkets ();
        const response = await this.marketGetGetmarketsummaries (params);
        //
        // {
        //     "success": "true",
        //     "message": "",
        //     "result": [
        //       {
        //         "MarketName":"KNOW-BTC",
        //         "High":0.00001313,
        //         "Low":0.0000121,
        //         "BaseVolume":24.06681016,
        //         "Last":0.00001253,
        //         "TimeStamp":"2018-07-10T07:44:56.936Z",
        //         "Volume":1920735.0486831602,
        //         "Bid":"0.00001260",
        //         "Ask":"0.00001242",
        //         "PrevDay":0.00001253
        //       },
        //       {
        //         "MarketName":"KNOW-ETH",
        //         "High":0.00018348,
        //         "Low":0.00015765,
        //         "BaseVolume":244.82775523,
        //         "Last":0.00017166,
        //         "TimeStamp":"2018-07-10T07:46:47.958Z",
        //         "Volume":1426236.4862518935,
        //         "Bid":"0.00017663",
        //         "Ask":"0.00017001",
        //         "PrevDay":0.00017166,
        //       },
        //       ...
        //     ],
        //     "volumes": [
        //       {
        //         "CoinName":"BTC",
        //         "Volume":571.64749041
        //       },
        //       {
        //         "CoinName":"KNOW",
        //         "Volume":19873172.0273
        //       }
        //     ],
        //     "t": 1531208813959;
        //   }
        //
        const result = this.safeValue (response, 'result');
        const tickers = [];
        for (let i = 0; i < result.length; i++) {
            const ticker = this.parseTicker (result[i]);
            tickers.push (ticker);
        }
        return this.filterByArray (tickers, 'symbol', symbols);
    }

    parseTrade (trade, market = undefined) {
        const timestamp = trade['time'];
        let side = undefined;
        if (trade['isBuyerMaker'] === true) {
            side = 'buy';
        } else if (trade['isBuyerMaker'] === false) {
            side = 'sell';
        }
        const id = trade['id'];
        let symbol = undefined;
        if (market !== undefined) {
            symbol = market['symbol'];
        }
        let cost = undefined;
        const price = this.safeFloat (trade, 'price');
        const amount = this.safeFloat (trade, 'qty');
        if (amount !== undefined) {
            if (price !== undefined) {
                cost = price * amount;
            }
        }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'symbol': symbol,
            'id': id,
            'order': undefined,
            'type': 'limit',
            'takerOrMaker': undefined,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': undefined,
        };
    }

    async fetchTicker (symbol, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'market': market['id'],
        };
        const response = await this.marketGetGetmarketsummaries (this.extend (request, params));
        //
        // {
        //     "success": "true",
        //     "message": "",
        //     "result": [
        //       {
        //         "MarketName":"KNOW-BTC",
        //         "High":0.00001313,
        //         "Low":0.0000121,
        //         "BaseVolume":24.06681016,
        //         "Last":0.00001253,
        //         "TimeStamp":"2018-07-10T07:44:56.936Z",
        //         "Volume":1920735.0486831602,
        //         "Bid":"0.00001260",
        //         "Ask":"0.00001242",
        //         "PrevDay":0.00001253
        //       },
        //       {
        //         "MarketName":"KNOW-ETH",
        //         "High":0.00018348,
        //         "Low":0.00015765,
        //         "BaseVolume":244.82775523,
        //         "Last":0.00017166,
        //         "TimeStamp":"2018-07-10T07:46:47.958Z",
        //         "Volume":1426236.4862518935,
        //         "Bid":"0.00017663",
        //         "Ask":"0.00017001",
        //         "PrevDay":0.00017166,
        //       },
        //       ...
        //     ],
        //     "volumes": [
        //       {
        //         "CoinName":"BTC",
        //         "Volume":571.64749041
        //       },
        //       {
        //         "CoinName":"KNOW",
        //         "Volume":19873172.0273
        //       }
        //     ],
        //     "t": 1531208813959;
        //   }
        //
        const ticker = response['result'][0];
        return this.parseTicker (ticker, market);
    }

    async fetchTrades (symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'symbol': symbol.replace ('/', '_'),
        };
        const response = await this.v1GetHt (this.extend (request, params));
        //
        // {
        // "symbol":"KNOW_BTC",
        // "limit":100,
        // "history":[
        //     {
        //     "id":139638,
        //     "price":"0.00001723",
        //     "qty":"81.00000000",
        //     "isBuyerMaker":false,
        //     "time":1529262196270
        //     }
        // ],
        // "time":1529298130192
        // }
        //
        if ('history' in response) {
            if (response['history'] !== undefined) {
                return this.parseTrades (response['history'], market, since, limit);
            }
        }
        // throw new ExchangeError (this.id + ' fetchTrades() returned undefined response');
    }

    parseOHLCV (ohlcv, market = undefined, timeframe = '1d', since = undefined, limit = undefined) {
        const timestamp = this.parse8601 (ohlcv['T'] + '+00:00');
        return [
            timestamp,
            ohlcv['O'],
            ohlcv['H'],
            ohlcv['L'],
            ohlcv['C'],
            ohlcv['V'],
        ];
    }

    async fetchOHLCV (symbol, timeframe = '1m', since = undefined, limit = undefined, params = {}) {
        // https://engine2.kryptono.exchange/api/v1/cs?symbol=BTC_USDT&tt=1m
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'tickInterval': this.timeframes[timeframe],
            'marketName': market['id'],
        };
        const response = await this.v1GetCs (this.extend (request, params));
        if ('result' in response) {
            if (response['result']) {
                return this.parseOHLCVs (response['result'], market, timeframe, since, limit);
            }
        }
    }

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.implodeParams (this.urls['api'][api], {
            'hostname': this.hostname,
        }) + '/';
        if (api !== 'v2' && api !== 'v1' && api !== 'market') {
            url += this.version + '/';
        }
        const route = path.split ('/')[0];
        if (route === 'account') {
            this.checkRequiredCredentials ();
            url += path;
            const recvWindow = this.safeValue (params, 'recvWindow');
            const query = this.urlencode (this.extend ({
                'timestamp': this.milliseconds (),
                'recvWindow': recvWindow,
            }, params));
            const signature = this.hmac (this.encode (query), this.encode (this.secret));
            url += '?' + query;
            headers = {
                'Authorization': this.apiKey,
                'Signature': signature,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            };
        } else if (route === 'order') {
            this.checkRequiredCredentials ();
            url += path;
            if (method !== 'GET') {
                body = this.json (params);
            }
            const signature = this.hmac (this.encode (this.json (params)), this.encode (this.secret));
            headers = {
                'Authorization': this.apiKey,
                'Signature': signature,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            };
        } else { // public endpoints
            url += path;
            if (Object.keys (params).length) {
                url += '?' + this.urlencode (params);
            }
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }

    async request (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        const response = await this.fetch2 (path, api, method, params, headers, body);
        // a workaround for APIKEY_INVALID
        if ((api === 'account') || (api === 'market')) {
            this.options['hasAlreadyAuthenticatedSuccessfully'] = true;
        }
        return response;
    }
};
