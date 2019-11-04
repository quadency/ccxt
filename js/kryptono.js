'use strict';

//  ---------------------------------------------------------------------------

const Exchange = require ('./base/Exchange');
const { BadSymbol, ExchangeError, AuthenticationError, InvalidOrder, InsufficientFunds, OrderNotFound, PermissionDenied, OnMaintenance } = require ('./base/errors');
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
                'fetchOrder': false,
                'fetchTickers': true, // TODO : Check with doc for fetchTicker
                'fetchOrderBook': true,
                'fetchTrades': true,
                'fetchOHLCV': true,
                'fetchBalance': true,
                // TODO : Check all of these properties are there or not to make sure.
                'createMarketOrder': false,
                'fetchDepositAddress': false, // TODO: Check if it is available again to make sure.
                'fetchClosedOrders': false,
                'fetchMyTrades': 'emulated',
                'fetchOpenOrders': false,
                'withdraw': false,
                'fetchDeposits': false,
                'fetchWithdrawals': false,
                'fetchTransactions': false,
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
                    'v2': 'https://{hostname}/api/v2/',
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
                        'account/balances',
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
        const minQuotesMap = quotes.reduce ((acc, curr) => {
            acc[curr.currency_code] = {
                'min': curr.minimum_total_order,
                'max': undefined,
            };
            return acc;
        }, {});
        const base = this.safeValue (response, 'coins');
        const minBaseMap = base.reduce ((acc, curr) => {
            acc[curr.currency_code] = {
                'min': curr.minimum_order_amount,
                'max': undefined,
            };
            return acc;
        }, {});
        return symbols.map ((symbolObj) => {
            const [base, quote] = symbolObj.symbol.split (this.options['symbolSeparator']);
            return {
                'id': symbolObj.symbol,
                'symbol': `${base}/${quote}`,
                'base': base,
                'baseId': base,
                'quote': quote,
                'quoteId': quote,
                'active': symbolObj.allow_trading,
                'info': symbolObj,
                'precision': {
                    'amount': symbolObj.amount_limit_decimal,
                    'price': symbolObj.price_limit_decimal,
                },
                'limits': {
                    'amount': {
                        'min': minBaseMap[base] ? minBaseMap[base].min : undefined,
                        'max': undefined,
                    },
                    'price': {
                        'min': minQuotesMap[quote] ? minQuotesMap[quote].min : undefined,
                        'max': undefined,
                    },
                },
            };
        });
    }

    async fetchBalance (params = {}) {
        await this.loadMarkets ();
        const response = await this.v2GetAccountBalances (params);
        // const balances = this.safeValue (response, 'result');
        const result = { 'info': response };
        // const indexed = this.indexBy (balances, 'Currency');
        // const currencyIds = Object.keys (indexed);
        for (let i = 0; i < response.length; i++) {
            // const currencyId = response[i].currency_code;
            // const code = this.safeCurrencyCode (currencyId);
            const account = this.account ();
            // const balance = response[i].total;
            account['free'] = this.safeFloat (response[i], 'available');
            account['total'] = this.safeFloat (response[i], 'total');
            result[response[i].currency_code] = account;
        }
        return this.parseBalance (result);
    }

    async fetchOrderBook (symbol, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const request = {
            'symbol': symbol,
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
        return this.parseOrderBook (response, response.time);
    }

    async fetchCurrencies (params = {}) {
        const response = await this.v2GetExchangeInfo (params);
        //
        // {
        //     "timezone": "UTC",
        //     "server_time": 1530683054384,
        //     "rate_limits": [
        //       {
        //         "type": "REQUESTS",
        //         "interval": "MINUTE",
        //         "limit": 1000
        //       }
        //     ],
        //     "base_currencies": [
        //       {
        //         "currency_code": "KNOW",
        //         "minimum_total_order": "100"
        //       }
        //     ],
        //     "coins": [
        //       {
        //         "currency_code": "USDT",
        //         "name": "Tether",
        //         "minimum_order_amount": "1"
        //       }
        //     ],
        //     "symbols": [
        //       {
        //         "symbol": "GTO_ETH",
        //         "amount_limit_decimal": 0,
        //         "price_limit_decimal": 8,
        //         "allow_trading": true
        //       }
        //     ]
        //   }
        //
        const currencies = this.safeValue (response, 'coins', []);
        const result = {};
        for (let i = 0; i < currencies.length; i++) {
            const currency = currencies[i];
            const id = this.safeString (currency, 'currency_code');
            // TODO: will need to rethink the fees
            // to add support for multiple withdrawal/deposit methods and
            // differentiated fees for each particular method
            const code = this.safeCurrencyCode (id);
            const precision = 8; // default precision, todo: fix "magic constants"
            // const address = this.safeValue (currency, 'BaseAddress');
            const fee = this.safeFloat (currency, 'TxFee'); // todo: redesign
            result[code] = {
                'id': id,
                'code': code,
                'address': 'TODO', // TODO see the correct value.
                'info': currency,
                'type': 'TODO', // TODO see the correct value.
                'name': currency.name,
                'active': true, // TODO: see the correct value.
                'fee': 'TODO', // TODO: see the correct value.
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': Math.pow (10, -precision),
                        'max': undefined,
                    },
                    'price': {
                        'min': Math.pow (10, -precision),
                        'max': undefined,
                    },
                    'cost': {
                        'min': undefined,
                        'max': undefined,
                    },
                    'withdraw': {
                        'min': fee,
                        'max': undefined,
                    },
                },
            };
        }
        return result;
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
            'symbol': symbol,
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
                const history = response.history.map (item => ({ ...item, 'timestamp': item.time }));
                return this.parseTrades (history, market, since, limit);
            }
        }
        throw new ExchangeError (this.id + ' fetchTrades() returned undefined response');
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
        if (api !== 'v2' && api !== 'v3' && api !== 'v3public') {
            url += this.version + '/';
        }
        if (api === 'public') {
            url += api + '/' + method.toLowerCase () + path;
            if (Object.keys (params).length) {
                url += '?' + this.urlencode (params);
            }
        } else if (api === 'v3public') {
            url += path;
            if (Object.keys (params).length) {
                url += '?' + this.urlencode (params);
            }
        } else if (api === 'v2') {
            url += path;
            if (Object.keys (params).length) {
                url += '?' + this.urlencode (params);
            }
        } else if (api === 'v3') {
            url += path;
            if (Object.keys (params).length) {
                url += '?' + this.rawencode (params);
            }
            const contentHash = this.hash (this.encode (''), 'sha512', 'hex');
            const timestamp = this.milliseconds ().toString ();
            let auth = timestamp + url + method + contentHash;
            const subaccountId = this.safeValue (this.options, 'subaccountId');
            if (subaccountId !== undefined) {
                auth += subaccountId;
            }
            const signature = this.hmac (this.encode (auth), this.encode (this.secret), 'sha512');
            headers = {
                'Api-Key': this.apiKey,
                'Api-Timestamp': timestamp,
                'Api-Content-Hash': contentHash,
                'Api-Signature': signature,
            };
            if (subaccountId !== undefined) {
                headers['Api-Subaccount-Id'] = subaccountId;
            }
        } else {
            this.checkRequiredCredentials ();
            url += api + '/';
            if (((api === 'account') && (path !== 'withdraw')) || (path === 'openorders')) {
                url += method.toLowerCase ();
            }
            const request = {
                'apikey': this.apiKey,
            };
            const disableNonce = this.safeValue (this.options, 'disableNonce');
            if ((disableNonce === undefined) || !disableNonce) {
                request['nonce'] = this.nonce ();
            }
            url += path + '?' + this.urlencode (this.extend (request, params));
            const signature = this.hmac (this.encode (url), this.encode (this.secret), 'sha512');
            headers = { 'apisign': signature };
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
