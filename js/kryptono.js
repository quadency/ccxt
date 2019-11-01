'use strict';

//  ---------------------------------------------------------------------------

const Exchange = require('./base/Exchange');
const { BadSymbol, ExchangeError, ExchangeNotAvailable, AuthenticationError, InvalidOrder, InsufficientFunds, OrderNotFound, DDoSProtection, PermissionDenied, AddressPending, OnMaintenance } = require('./base/errors');
const { TRUNCATE, DECIMAL_PLACES } = require('./base/functions/number');

//  ---------------------------------------------------------------------------

module.exports = class kryptono extends Exchange {
    describe() {
        return this.deepExtend(super.describe(), {
            'id': 'kryptono',
            'name': 'Kryptono',
            'countries': ['SG'],
            'version': 'v2',
            'rateLimit': 1000, // TODO: Check if this is the corrrect as per CCXT requirments. Kryptono gives 1000 minute intervals.
            'certified': true,
            // new metainfo interface
            'has': {
                // TODO : Check all of these properties are there or not to make sure.
                'CORS': true,
                'fetchMarkets': true,
                'fetchCurrencies': true,
                'fetchTradingLimits': false,
                'fetchOrder': false,
                'fetchTickers': true, // TODO : Check with doc for fetchTicker
                'fetchOrderBook': true,
                'fetchTrades': true,
                'fetchOHLCV': true,
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
                    'https://p.kryptono.exchange/k/api'
                ],
                'fees': [
                    'https://kryptono.zendesk.com/hc/en-us/articles/360004347772-2-Fee-on-Kryptono-Exchange-'
                ],
            },
            'api': {
                'v2': {
                    'get': [
                        'exchange-info',
                        'market-price',
                    ],
                },
                'market': {
                    'get': [
                        'getmarketsummaries',
                    ],
                },
                'v1': {
                    'get': [
                        'dp',
                        'ht',
                    ],
                },
            },
            'exceptions': {
                // 'Call to Cancel was throttled. Try again in 60 seconds.': DDoSProtection,
                // 'Call to GetBalances was throttled. Try again in 60 seconds.': DDoSProtection,
                'APISIGN_NOT_PROVIDED': AuthenticationError,
                'INVALID_SIGNATURE': AuthenticationError,
                'INVALID_CURRENCY': ExchangeError,
                'INVALID_PERMISSION': AuthenticationError,
                'INSUFFICIENT_FUNDS': InsufficientFunds,
                'QUANTITY_NOT_PROVIDED': InvalidOrder,
                'MIN_TRADE_REQUIREMENT_NOT_MET': InvalidOrder,
                'ORDER_NOT_OPEN': OrderNotFound,
                'INVALID_ORDER': InvalidOrder,
                'UUID_INVALID': OrderNotFound,
                'RATE_NOT_PROVIDED': InvalidOrder, // createLimitBuyOrder ('ETH/BTC', 1, 0)
                'WHITELIST_VIOLATION_IP': PermissionDenied,
                'DUST_TRADE_DISALLOWED_MIN_VALUE': InvalidOrder,
                'RESTRICTED_MARKET': BadSymbol,
                'We are down for scheduled maintenance, but we\u2019ll be back up shortly.': OnMaintenance, // {"success":false,"message":"We are down for scheduled maintenance, but we\u2019ll be back up shortly.","result":null,"explanation":null}
            }
        });
    }

    costToPrecision(symbol, cost) {
        return this.decimalToPrecision(cost, TRUNCATE, this.markets[symbol]['precision']['price'], DECIMAL_PLACES);
    }

    feeToPrecision(symbol, fee) {
        return this.decimalToPrecision(fee, TRUNCATE, this.markets[symbol]['precision']['price'], DECIMAL_PLACES);
    }

    async fetchMarkets(params = {}) {
        const response = await this.v2GetMarketPrice(params);
        //
        //     [
        //         {
        //             "symbol":"LTC-BTC",
        //             "baseCurrencySymbol":"LTC",
        //             "quoteCurrencySymbol":"BTC",
        //             "minTradeSize":"0.01686767",
        //             "precision":8,
        //             "status":"ONLINE", // "OFFLINE"
        //             "createdAt":"2014-02-13T00:00:00Z"
        //         },
        //         {
        //             "symbol":"VDX-USDT",
        //             "baseCurrencySymbol":"VDX",
        //             "quoteCurrencySymbol":"USDT",
        //             "minTradeSize":"300.00000000",
        //             "precision":8,
        //             "status":"ONLINE", // "OFFLINE"
        //             "createdAt":"2019-05-23T00:41:21.843Z",
        //             "notice":"USDT has swapped to an ERC20-based token as of August 5, 2019."
        //         }
        //     ]
        //
        const result = [];
        // const markets = this.safeValue (response, 'result');
        for (let i = 0; i < response.length; i++) {
            const market = response[i];
            const name = this.safeString(market, 'symbol');
            const baseId = name.split('_')[1];
            const quoteId = name.split('_')[0];
            const id = quoteId + this.options['symbolSeparator'] + baseId;
            const base = this.safeCurrencyCode(baseId);
            const quote = this.safeCurrencyCode(quoteId);
            const symbol = base + '/' + quote;
            const pricePrecision = this.safeInteger(market, 'precision', 8);
            const precision = {
                'amount': 8,
                'price': pricePrecision,
            };
            const status = this.safeString(market, 'status');
            const active = (status === 'ONLINE');
            result.push({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'info': market,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': this.safeFloat(market, 'minTradeSize'),
                        'max': undefined,
                    },
                    'price': {
                        'min': Math.pow(10, -precision['price']),
                        'max': undefined,
                    },
                },
            });
        }
        return result;
    }

    // async fetchBalance (params = {}) {
    //     await this.loadMarkets ();
    //     const response = await this.accountGetBalances (params);
    //     const balances = this.safeValue (response, 'result');
    //     const result = { 'info': balances };
    //     const indexed = this.indexBy (balances, 'Currency');
    //     const currencyIds = Object.keys (indexed);
    //     for (let i = 0; i < currencyIds.length; i++) {
    //         const currencyId = currencyIds[i];
    //         const code = this.safeCurrencyCode (currencyId);
    //         const account = this.account ();
    //         const balance = indexed[currencyId];
    //         account['free'] = this.safeFloat (balance, 'Available');
    //         account['total'] = this.safeFloat (balance, 'Balance');
    //         result[code] = account;
    //     }
    //     return this.parseBalance (result);
    // }

    async fetchOrderBook(symbol, limit = undefined, params = {}) {
        await this.loadMarkets();
        const request = {
            'symbol': symbol,
        };
        const response = await this.v1GetDp(this.extend(request, params));
        return this.parseOrderBook(response, response.time);
    }

    async fetchCurrencies(params = {}) {
        const response = await this.v2GetExchangeInfo(params);
        //
        //     {
        //         "success": true,
        //         "message": "",
        //         "result": [
        //             {
        //                 "Currency": "BTC",
        //                 "CurrencyLong":"Bitcoin",
        //                 "MinConfirmation":2,
        //                 "TxFee":0.00050000,
        //                 "IsActive":true,
        //                 "IsRestricted":false,
        //                 "CoinType":"BITCOIN",
        //                 "BaseAddress":"1N52wHoVR79PMDishab2XmRHsbekCdGquK",
        //                 "Notice":null
        //             },
        //             ...,
        //         ]
        //     }
        //
        const currencies = this.safeValue(response, 'coins', []);
        const result = {};
        for (let i = 0; i < currencies.length; i++) {
            const currency = currencies[i];
            const id = this.safeString(currency, 'currency_code');
            // TODO: will need to rethink the fees
            // to add support for multiple withdrawal/deposit methods and
            // differentiated fees for each particular method
            const code = this.safeCurrencyCode(id);
            const precision = 8; // default precision, todo: fix "magic constants"
            // const address = this.safeValue (currency, 'BaseAddress');
            const fee = this.safeFloat(currency, 'TxFee'); // todo: redesign
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
                        'min': Math.pow(10, -precision),
                        'max': undefined,
                    },
                    'price': {
                        'min': Math.pow(10, -precision),
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

    parseTicker(ticker, market = undefined) {
        //
        //     {
        //         "MarketName":"BTC-ETH",
        //         "High":0.02127099,
        //         "Low":0.02035064,
        //         "Volume":10288.40271571,
        //         "Last":0.02070510,
        //         "BaseVolume":214.64663206,
        //         "TimeStamp":"2019-09-18T21:03:59.897",
        //         "Bid":0.02070509,
        //         "Ask":0.02070510,
        //         "OpenBuyOrders":1228,
        //         "OpenSellOrders":5899,
        //         "PrevDay":0.02082823,
        //         "Created":"2015-08-14T09:02:24.817"
        //     }
        //
        const timestamp = this.parse8601(this.safeString(ticker, 'TimeStamp'));
        let symbol = undefined;
        const marketId = this.safeString(ticker, 'MarketName');
        if (marketId !== undefined) {
            if (marketId in this.markets_by_id) {
                market = this.markets_by_id[marketId];
            } else {
                symbol = this.parseSymbol(marketId);
            }
        }
        if ((symbol === undefined) && (market !== undefined)) {
            symbol = market['symbol'];
        }
        const previous = this.safeFloat(ticker, 'PrevDay');
        const last = this.safeFloat(ticker, 'Last');
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
            'datetime': this.iso8601(timestamp),
            'high': this.safeFloat(ticker, 'High'),
            'low': this.safeFloat(ticker, 'Low'),
            'bid': this.safeFloat(ticker, 'Bid'),
            'bidVolume': undefined,
            'ask': this.safeFloat(ticker, 'Ask'),
            'askVolume': undefined,
            'vwap': undefined,
            'open': previous,
            'close': last,
            'last': last,
            'previousClose': undefined,
            'change': change,
            'percentage': percentage,
            'average': undefined,
            'baseVolume': this.safeFloat(ticker, 'Volume'),
            'quoteVolume': this.safeFloat(ticker, 'BaseVolume'),
            'info': ticker,
        };
    }

    async fetchTickers(symbols = undefined, params = {}) {
        await this.loadMarkets();
        const response = await this.marketGetGetmarketsummaries(params);
        const result = this.safeValue(response, 'result');
        const tickers = [];
        for (let i = 0; i < result.length; i++) {
            const ticker = this.parseTicker(result[i]);
            tickers.push(ticker);
        }
        return this.filterByArray(tickers, 'symbol', symbols);
    }

    async fetchTicker(symbol, params = {}) {
        await this.loadMarkets();
        const market = this.market(symbol);
        const request = {
            'market': market['id'],
        };
        const response = await this.marketGetGetmarketsummaries(this.extend(request, params));
        //
        //     {
        //         "success":true,
        //         "message":"",
        //         "result":[
        //             {
        //                 "MarketName":"BTC-ETH",
        //                 "High":0.02127099,
        //                 "Low":0.02035064,
        //                 "Volume":10288.40271571,
        //                 "Last":0.02070510,
        //                 "BaseVolume":214.64663206,
        //                 "TimeStamp":"2019-09-18T21:03:59.897",
        //                 "Bid":0.02070509,
        //                 "Ask":0.02070510,
        //                 "OpenBuyOrders":1228,
        //                 "OpenSellOrders":5899,
        //                 "PrevDay":0.02082823,
        //                 "Created":"2015-08-14T09:02:24.817"
        //             }
        //         ]
        //     }
        //
        const ticker = response['result'][0];
        return this.parseTicker(ticker, market);
    }

    async fetchTrades(symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets();
        const market = this.market(symbol);
        const request = {
            'symbol': symbol,
        };
        const response = await this.v1GetHt(this.extend(request, params));
        if ('history' in response) {
            if (response['history'] !== undefined) {
                const history = response.history.map((item) => {
                    return { ...item, 'timestamp': item.time };
                });
                return this.parseTrades(history, market, since, limit);
            }
        }
        throw new ExchangeError(this.id + ' fetchTrades() returned undefined response');
    }
    parseOHLCV(ohlcv, market = undefined, timeframe = '1d', since = undefined, limit = undefined) {
        const timestamp = this.parse8601(ohlcv['T'] + '+00:00');
        return [
            timestamp,
            ohlcv['O'],
            ohlcv['H'],
            ohlcv['L'],
            ohlcv['C'],
            ohlcv['V'],
        ];
    }
    async fetchOHLCV(symbol, timeframe = '1m', since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets();
        const market = this.market(symbol);
        const request = {
            'tickInterval': this.timeframes[timeframe],
            'marketName': market['id'],
        };
        const response = await this.v2GetMarketGetTicks(this.extend(request, params));
        if ('result' in response) {
            if (response['result']) {
                return this.parseOHLCVs(response['result'], market, timeframe, since, limit);
            }
        }
    }

    sign(path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.implodeParams(this.urls['api'][api], {
            'hostname': this.hostname,
        }) + '/';
        if (api !== 'v2' && api !== 'v3' && api !== 'v3public') {
            url += this.version + '/';
        }
        if (api === 'public') {
            url += api + '/' + method.toLowerCase() + path;
            if (Object.keys(params).length) {
                url += '?' + this.urlencode(params);
            }
        } else if (api === 'v3public') {
            url += path;
            if (Object.keys(params).length) {
                url += '?' + this.urlencode(params);
            }
        } else if (api === 'v2') {
            url += path;
            if (Object.keys(params).length) {
                url += '?' + this.urlencode(params);
            }
        } else if (api === 'v3') {
            url += path;
            if (Object.keys(params).length) {
                url += '?' + this.rawencode(params);
            }
            const contentHash = this.hash(this.encode(''), 'sha512', 'hex');
            const timestamp = this.milliseconds().toString();
            let auth = timestamp + url + method + contentHash;
            const subaccountId = this.safeValue(this.options, 'subaccountId');
            if (subaccountId !== undefined) {
                auth += subaccountId;
            }
            const signature = this.hmac(this.encode(auth), this.encode(this.secret), 'sha512');
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
            this.checkRequiredCredentials();
            url += api + '/';
            if (((api === 'account') && (path !== 'withdraw')) || (path === 'openorders')) {
                url += method.toLowerCase();
            }
            const request = {
                'apikey': this.apiKey,
            };
            const disableNonce = this.safeValue(this.options, 'disableNonce');
            if ((disableNonce === undefined) || !disableNonce) {
                request['nonce'] = this.nonce();
            }
            url += path + '?' + this.urlencode(this.extend(request, params));
            const signature = this.hmac(this.encode(url), this.encode(this.secret), 'sha512');
            headers = { 'apisign': signature };
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }

    async request(path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        const response = await this.fetch2(path, api, method, params, headers, body);
        // a workaround for APIKEY_INVALID
        if ((api === 'account') || (api === 'market')) {
            this.options['hasAlreadyAuthenticatedSuccessfully'] = true;
        }
        return response;
    }
};
