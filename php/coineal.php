<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import
use \ccxt\ExchangeError;
use \ccxt\ArgumentsRequired;
use \ccxt\InvalidOrder;

class coineal extends Exchange {

    public function describe () {
        return array_replace_recursive(parent::describe (), array(
            'id' => 'coineal',
            'name' => 'Coineal',
            'countries' => array(),
            'rateLimit' => 1000,
            'has' => array(
                'fetchMarkets' => true,
                'fetchOHLCV' => true,
                'fetchOrderBook' => true,
                'fetchTrades' => true,
                'createOrder' => true,
                'cancelOrder' => true,
                'fetchMyTrades' => true,
                'fetchOpenOrders' => true,
                'fetchBalance' => true,
                'fetchOrder' => true,
                'fetchClosedOrders' => true,
                'fetchTicker' => true,
                'fetchOrders' => true,
            ),
            'timeframes' => array(
                '1m' => '1', // default
                '5m' => '5',
                '15m' => '15',
                '30m' => '30',
                '1h' => '60',
                '1d' => '1440',
            ),
            'urls' => array(
                'api' => array(
                    'public' => 'https://exchange-open-api.coineal.com',
                    'private' => 'https://exchange-open-api.coineal.com',
                ),
                'www' => 'https://exchange-open-api.coineal.com',
            ),
            'api' => array(
                'public' => array(
                    'get' => array(
                        'open/api/common/symbols',
                        'open/api/get_records',
                        'open/api/market_dept',
                        'open/api/get_trades',
                        'open/api/get_ticker',
                    ),
                ),
                'private' => array(
                    'get' => array(
                        'open/api/all_trade',
                        'open/api/new_order',
                        'open/api/user/account',
                        'open/api/order_info',
                    ),
                    'post' => array(
                        'open/api/create_order',
                        'open/api/cancel_order',
                    ),
                ),
            ),
            'exceptions' => array(
                '5' => '\\ccxt\\InvalidOrder',
                '6' => '\\ccxt\\InvalidOrder',
                '7' => '\\ccxt\\InvalidOrder',
                '8' => '\\ccxt\\InvalidOrder',
                '19' => '\\ccxt\\InsufficientFunds',
                '22' => '\\ccxt\\OrderNotFound',
                '23' => '\\ccxt\\ArgumentsRequired',
                '24' => '\\ccxt\\ArgumentsRequired',
                '100004' => '\\ccxt\\BadRequest',
                '100005' => '\\ccxt\\BadRequest',
                '100007' => '\\ccxt\\AuthenticationError',
                '110002' => '\\ccxt\\BadSymbol',
                '110005' => '\\ccxt\\InsufficientFunds',
                '110032' => '\\ccxt\\AuthenticationError',
            ),
            'errorMessages' => array(
                '5' => 'Order Failed',
                '6' => 'Exceed the minimum volume requirement',
                '7' => 'Exceed the maximum volume requirement',
                '8' => 'Order cancellation failed',
                '9' => 'The transaction is frozen',
                '13' => 'Sorry, the program has a system error, please contact the webmaster',
                '19' => 'Insufficient balance available',
                '22' => 'Order does not exist',
                '23' => 'Missing transaction quantity parameter',
                '24' => 'Missing transaction price parameter',
                '25' => 'Quantity Precision Error',
                '100001' => 'System error',
                '100002' => 'System upgrade',
                '100004' => 'Parameter request is invalid',
                '100005' => 'Parameter signature error',
                '100007' => 'Unathorized IP',
                '110002' => 'Unknown currency code',
                '110005' => 'Insufficient balance available',
                '110025' => 'Account locked by background administrator',
                '110032' => 'This user is not athorized to do this',
            ),
        ));
    }

    public function sign ($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $url = $this->urls['api'][$api];
        $url .= '/' . $path;
        $query = $this->omit ($params, $this->extract_params($path));
        if ($api === 'private') {
            $content = '';
            $query['api_key'] = $this->apiKey;
            $sortedParams = $this->keysort ($query);
            $keys = is_array($sortedParams) ? array_keys($sortedParams) : array();
            for ($i = 0; $i < count($keys); $i++) {
                $key = $keys[$i];
                $content .= $key . (string) $sortedParams[$key];
            }
            $signature = $content . $this->secret;
            $hash = $this->hash ($this->encode ($signature), 'md5');
            $query['sign'] = $hash;
            if ($method === 'POST') {
                $headers = array(
                    'Content-Type' => 'application/x-www-form-urlencoded',
                );
            }
        }
        if ($query) {
            $url .= '?' . $this->urlencode ($query);
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function fetch_markets ($params = array ()) {
        $response = $this->publicGetOpenApiCommonSymbols ();
        // Exchange $response
        // {
        //     "code" => "0",
        //     "msg" => "suc",
        //     "data" => array(
        //         {
        //             "$symbol" => "btcusdt",
        //             "count_coin" => "usdt",
        //             "amount_precision" => 5,
        //             "base_coin" => "btc",
        //             "price_precision" => 2
        //         }
        //     )
        // }
        $result = array();
        $markets = $this->safe_value($response, 'data');
        for ($i = 0; $i < count($markets); $i++) {
            $market = $markets[$i];
            $id = $this->safe_string($market, 'symbol');
            $baseId = $this->safe_string($market, 'base_coin');
            $quoteId = $this->safe_string($market, 'count_coin');
            $base = $this->safe_currency_code($baseId);
            $quote = $this->safe_currency_code($quoteId);
            $symbol = $base . '/' . $quote;
            $precision = array(
                'amount' => $this->safe_integer($market, 'amount_precision'),
                'price' => $this->safe_integer($market, 'price_precision'),
            );
            $active = true;
            $entry = array(
                'id' => $id,
                'symbol' => $symbol,
                'base' => $base,
                'quote' => $quote,
                'baseId' => $baseId,
                'quoteId' => $quoteId,
                'info' => $market,
                'active' => $active,
                'precision' => $precision,
                'limits' => array(
                    'amount' => array(
                        'min' => pow(10, -$precision['amount']),
                        'max' => null,
                    ),
                    'price' => array(
                        'min' => null,
                        'max' => null,
                    ),
                    'cost' => array(
                        'min' => null,
                        'max' => null,
                    ),
                ),
            );
            $result[] = $entry;
        }
        return $result;
    }

    public function parse_ohlcv ($ohlcv, $market = null, $timeframe = '1m', $since = null, $limit = null) {
        return [
            $ohlcv[0] * 1000,
            floatval ($ohlcv[1]),
            floatval ($ohlcv[3]),
            floatval ($ohlcv[4]),
            floatval ($ohlcv[2]),
            floatval ($ohlcv[5]),
        ];
    }

    public function fetch_ohlcv ($symbol = 'BTC/USDT', $timeframe = '1m', $params = array (), $since = null, $limit = null) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
            'period' => $this->timeframes[$timeframe],
        );
        $response = $this->publicGetOpenApiGetRecords (array_merge($request, $params));
        // Exchange $response
        // {
        //     'code' => '0',
        //     'msg' => 'suc',
        //     'data' => array(
        //                 array(
        //                     1529387760,  //Time Stamp
        //                     7585.41,  //Opening Price
        //                     7585.41,  //Highest Price
        //                     7585.41,  //Lowest Price
        //                     7585.41,  //Closing Price
        //                     0.0       //Transaction Volume
        //                 )
        //             )
        // }
        return $this->parse_ohlcvs($this->safe_value($response, 'data'), $market, $timeframe, $since, $limit);
    }

    public function fetch_order_book ($symbol = 'BTC/USDT', $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
            'type' => 'step0',
        );
        $response = $this->publicGetOpenApiMarketDept (array_merge($request, $params));
        // Exchange $response
        // {
        //     "code" => "0",
        //     "msg" => "suc",
        //     "$data" => {
        //         "tick" => {
        //             "time" => 1529408112000,  //Refresh time of depth
        //             "asks" => //Ask orders
        //             array(
        //                 array(
        //                     "6753.31", //Price of Ask 1
        //                     0.00306    //Order Size of Ask 1
        //                 ),
        //                 array(
        //                     "6754.78", //Price of Ask 2
        //                     0.61112   //Order Size of Ask 2
        //                 )
        //                 ...
        //             ),
        //             "bids" => //Ask orders
        //             array(
        //                 array(
        //                     "6732.02",  //Price of Bid 1
        //                     0.18444     //Order Size of Bid 1
        //                 ),
        //                 array(
        //                     "6730.08", //Price of Bid 2
        //                     0.14662    //Order Size of Bid 2
        //                 )
        //                 ...
        //             )
        //         }
        $data = $this->safe_value($response, 'data');
        $detailData = $this->safe_value($data, 'tick');
        return $this->parse_order_book($detailData, $this->safe_value($detailData, 'time'));
    }

    public function parse_ticker ($ticker, $market = null) {
        $timestamp = $this->safe_integer($ticker, 'time');
        $symbol = null;
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        $last = $this->safe_float($ticker, 'last');
        return array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'high' => $this->safe_float($ticker, 'high'),
            'low' => $this->safe_float($ticker, 'low'),
            'bid' => null,
            'bidVolume' => null,
            'ask' => null,
            'askVolume' => null,
            'vwap' => null,
            'open' => null,
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => null,
            'percentage' => null,
            'average' => null,
            'baseVolume' => $this->safe_float($ticker, 'vol'),
            'quoteVolume' => null,
            'info' => $ticker,
        );
    }

    public function fetch_ticker ($symbol, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
        );
        $response = $this->publicGetOpenApiGetTicker (array_merge($request));
        // {
        //     "code" => "0",
        //     "msg" => "suc",
        //     "data" => {
        //         "high" => 6796.63,
        //         "vol" => 2364.85442742,
        //         "last" => 6722.37,
        //         "low" => 6399.28,
        //         "buy" => "6721.56",
        //         "sell" => "6747.47",
        //         "time" => 1529406706715
        //     }
        // }
        $result = $this->safe_value($response, 'data');
        return $this->parse_ticker($result, $market);
    }

    public function parse_trade ($trade, $market = null) {
        // Fetch Trades Object When Symbol is Undefined
        //             {
        //                 "volume" => "1.000",
        //                 "$side" => "BUY",
        //                 "$price" => "0.10000000",
        //                 "$fee" => "0.16431104",
        //                 "ctime" => 1510996571195,
        //                 "deal_price" => "0.10000000",
        //                 "id" => 306,
        //                 "type" => "买入",
        //                 "$market" => "marketObj"
        //             }
        // Fetch My Trades Object
        //             {
        //                 "volume" => "1.000",
        //                 "$side" => "BUY",
        //                 "$price" => "0.10000000",
        //                 "$fee" => "0.16431104",
        //                 "ctime" => 1510996571195,
        //                 "deal_price" => "0.10000000",
        //                 "id" => 306,
        //                 "type" => "买入"
        //             }
        // Fetch Trades Object
        //         {
        //             "$amount" => 0.99583,
        //             "trade_time" => 1529408112000,
        //             "$price" => 6763.9,
        //             "id" => 280101,
        //             "type" => "sell"
        //         }
        $timestamp = $this->safe_string($trade, 'trade_time');
        if ($timestamp === null) {
            $timestamp = $this->safe_string($trade, 'ctime');
        }
        $price = $this->safe_float($trade, 'price');
        $amount = $this->safe_float($trade, 'amount');
        if ($amount === null) {
            $amount = $this->safe_float($trade, 'volume');
        }
        $symbol = null;
        if ($market === null) {
            $market = $this->safe_value($trade, 'market');
        }
        if ($market !== null) {
            $symbol = $this->safe_string($market, 'symbol');
        }
        $cost = null;
        if ($price !== null) {
            if ($amount !== null) {
                if ($symbol !== null) {
                    $cost = floatval ($this->cost_to_precision($symbol, $price * $amount));
                }
            }
        }
        $side = $this->safe_string($trade, 'side');
        if ($side === null) {
            $side = $this->safe_string($trade, 'type');
        }
        $transactionId = null;
        if ($side !== null) {
            if (strtoupper($side) === 'BUY') {
                $transactionId = $this->safe_string($trade, 'bid_id');
            }
            if (strtoupper($side) === 'SELL') {
                $transactionId = $this->safe_string($trade, 'ask_id');
            }
        }
        if ($transactionId === null) {
            $transactionId = $this->safe_string($trade, 'id');
        }
        $feecost = $this->safe_float($trade, 'fee');
        $fee = null;
        if ($feecost !== null) {
            $fee = array(
                'cost' => $feecost,
                'currency' => $this->safe_string($trade, 'feeCoin'),
            );
        }
        return array(
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'symbol' => $symbol,
            'id' => $transactionId,
            'order' => $transactionId,
            'type' => null,
            'side' => $side,
            'takerOrMaker' => null,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'fee' => $fee,
        );
    }

    public function fetch_trades ($symbol = 'BTC/USDT', $params = array (), $since = null, $limit = null) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
        );
        $response = $this->publicGetOpenApiGetTrades (array_merge($request, $params));
        // Exchange $response
        // {
        //     "code" => "0",
        //     "msg" => "suc",
        //     "data" => array(
        //         {
        //             "amount" => 0.99583,
        //             "trade_time" => 1529408112000,
        //             "price" => 6763.9,
        //             "id" => 280101,
        //             "type" => "sell"
        //         }
        //     )
        // }
        return $this->parse_trades($this->safe_value($response, 'data'), $market, $since, $limit);
    }

    public function create_order ($symbol, $type, $side, $amount, $price = null, $params = null) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'time' => (string) $this->milliseconds (),
            'symbol' => $market['id'],
            'side' => strtoupper($side),
            'volume' => $amount,
        );
        if ($type === 'limit') {
            $request['type'] = '1';
            $request['price'] = $this->price_to_precision($symbol, $price);
        } else {
            $request['type'] = '2';
            if (strtoupper($side) === 'BUY') {
                $currentSymbolDetail = $this->fetch_ticker($symbol);
                $currentPrice = $this->safe_float($currentSymbolDetail, 'last');
                if ($currentPrice === null) {
                    throw new InvalidOrder('Provide correct Symbol');
                }
                $request['volume'] = $this->cost_to_precision($symbol, $amount * $currentPrice);
            }
        }
        $response = $this->privatePostOpenApiCreateOrder (array_merge($request, $params));
        // Exchange $response
        // {
        //     "$code" => "0",
        //     "msg" => "suc",
        //     "data" => {
        //         "order_id" => 34343
        //     }
        // }
        $code = $this->safe_string($response, 'code');
        if ($code !== '0') {
            throw new InvalidOrder($response['msg'] . ' ' . $this->json ($response));
        }
        $result = $this->safe_value($response, 'data');
        return $this->fetch_order($this->safe_string($result, 'order_id'), $symbol);
    }

    public function cancel_order ($id, $symbol = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' CancelOrder requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
            'order_id' => $id,
            'time' => $this->milliseconds (),
        );
        $response = $this->privatePostOpenApiCancelOrder (array_merge($request, $params));
        // Exchange $response
        // {
        //     "$code" => "0",
        //     "msg" => "suc",
        //     "data" => array()
        // }
        $code = $this->safe_string($response, 'code');
        if ($code !== '0') {
            throw new InvalidOrder($response['msg'] . ' ' . $this->json ($response));
        }
        return $this->fetch_order($id, $symbol);
    }

    public function get_trades ($symbol, $limit, $params) {
        $request = array(
            'symbol' => $symbol,
            'time' => $this->milliseconds (),
            'page' => 1,
            'pageSize' => $limit,
        );
        $response = $this->privateGetOpenApiAllTrade (array_merge($request, $params));
        $result = $this->safe_value($response, 'data');
        return $this->safe_value($result, 'resultList', array());
    }

    public function fetch_my_trades ($symbol = null, $since = null, $limit = 100, $params = array ()) {
        $this->load_markets();
        // Exchange response
        // {
        //     "code" => "0",
        //     "msg" => "suc",
        //     "data" => {
        //         "count" => 22,
        //         "resultList" => array(
        //             {
        //                 "volume" => "1.000",
        //                 "side" => "BUY",
        //                 "price" => "0.10000000",
        //                 "fee" => "0.16431104",
        //                 "ctime" => 1510996571195,
        //                 "deal_price" => "0.10000000",
        //                 "id" => 306,
        //                 "type" => "买入",
        //             }
        //         )
        //     }
        // }
        if ($symbol === null) {
            $totalMarkets = is_array($this->markets) ? array_keys($this->markets) : array();
            $trades = array();
            for ($i = 0; $i < count($totalMarkets); $i++) {
                $market = $this->market ($totalMarkets[$i]);
                $result = $this->get_trades ($market['id'], $limit, $params);
                for ($i = 0; $i < count($result); $i++) {
                    $result[$i]['market'] = $market;
                }
                $trades = $this->array_concat($trades, $result);
            }
            return $this->parse_trades($trades, null, $since, $limit);
        }
        $market = $this->market ($symbol);
        $result = $this->get_trades ($market['id'], $limit, $params);
        return $this->parse_trades($result, $market, $since, $limit);
    }

    public function parse_order_status ($status) {
        $statuses = array(
            '0' => 'Open', // Historical Order Unsuccessful
            '1' => 'Open',
            '2' => 'Closed',
            '3' => 'Open', // Partially Opened
            '4' => 'Cancelled',
            '5' => 'Cancelling',
            '6' => 'Abnormal Orders',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_order ($order, $market = null) {
        $status = $this->parse_order_status($this->safe_string($order, 'status'));
        $symbol = null;
        $baseId = $this->safe_string($order, 'baseCoin');
        $quoteId = $this->safe_string($order, 'countCoin');
        $base = $this->safe_currency_code($baseId); // unified
        $quote = $this->safe_currency_code($quoteId);
        if ($base !== null) {
            if ($quote !== null) {
                $symbol = $base . '/' . $quote;
            }
        }
        $timestamp = $this->safe_string($order, 'created_at');
        $filled = $this->safe_float($order, 'deal_volume');
        $remaining = $this->safe_float($order, 'remain_volume');
        $amount = $this->safe_float($order, 'volume');
        if ($filled !== null) {
            if ($remaining !== null) {
                $amount = $this->amount_to_precision($symbol, $filled . $remaining);
            }
        }
        $id = $this->safe_string($order, 'order_id');
        if ($id === null) {
            $id = $this->safe_string($order, 'id');
        }
        $side = $this->safe_string($order, 'side');
        $cost = null;
        $type = null;
        $typeId = $this->safe_integer($order, 'type');
        if ($typeId !== null) {
            if ($typeId === 1) {
                $type = 'limit';
            } else {
                $type = 'market';
            }
        }
        $trades = $this->safe_value($order, 'tradeList');
        $price = $this->safe_float($order, 'total_price');
        if ($type === 'limit') {
            $price = $this->safe_float($order, 'price');
        }
        if ($trades !== null) {
            if (strlen($trades) > 0) {
                $price = $this->safe_float($order, 'avg_price');
            }
        }
        if ($filled !== null) {
            if ($price !== null) {
                $cost = $filled * $price;
            }
        }
        $fee = null;
        $average = $this->safe_float($order, 'avg_price');
        if ($trades !== null) {
            $trades = $this->parse_trades($trades, $market);
            $feeCost = null;
            $numTrades = is_array($trades) ? count($trades) : 0;
            for ($i = 0; $i < $numTrades; $i++) {
                if ($feeCost === null) {
                    $feeCost = 0;
                }
                $tradeFee = $this->safe_float($trades[$i], 'fee');
                if ($tradeFee !== null) {
                    $feeCost = $this->sum ($feeCost, $tradeFee);
                }
            }
            $feeCurrency = null;
            if ($market !== null) {
                $feeCurrency = $market['quote'];
            }
            if ($feeCost !== null) {
                $fee = array(
                    'cost' => $feeCost,
                    'currency' => $feeCurrency,
                );
            }
        }
        return array(
            'info' => $order,
            'id' => $id,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'lastTradeTimestamp' => null,
            'symbol' => $symbol,
            'type' => $type,
            'side' => $side,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'average' => $average,
            'filled' => $filled,
            'remaining' => $remaining,
            'status' => $status,
            'fee' => $fee,
            'trades' => $trades,
        );
    }

    public function fetch_common_orders ($symbol, $limit, $params) {
        $request = array(
            'symbol' => $symbol,
            'time' => $this->milliseconds (),
            'page' => 1,
            'pageSize' => $limit,
        );
        $response = $this->privateGetOpenApiNewOrder (array_merge($request, $params));
        $result = $this->safe_value($response, 'data');
        return $this->safe_value($result, 'resultList', array());
    }

    public function fetch_closed_orders ($symbol = null, $since = null, $limit = 100, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' FetchOpenOrder requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $orderData = $this->fetch_common_orders ($market['id'], $limit, $params);
        $closedOrdered = $this->filter_by($orderData, 'status', 2);
        return $this->parse_orders($closedOrdered, $market, $since, $limit);
    }

    public function fetch_open_orders ($symbol = null, $since = null, $limit = 100, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' FetchOpenOrder requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $orderData = $this->fetch_common_orders ($market['id'], $limit, $params);
        // Exchange response
        // {
        //     "code" => "0",
        //     "msg" => "suc",
        //     "data" => {
        //         "count" => 10,
        //         "resultList" => array(
        //             {
        //                 "side" => "BUY",
        //                 "total_price" => "0.10000000",
        //                 "created_at" => 1510993841000,
        //                 "avg_price" => "0.10000000",
        //                 "countCoin" => "btc",
        //                 "source" => 1,
        //                 "type" => 1,
        //                 "side_msg" => "买入",
        //                 "volume" => "1.000",
        //                 "price" => "0.10000000",
        //                 "source_msg" => "WEB",
        //                 "status_msg" => "部分成交",
        //                 "deal_volume" => "0.50000000",
        //                 "id" => 424,
        //                 "remain_volume" => "0.00000000",
        //                 "baseCoin" => "eth",
        //                 "tradeList" => array(
        //                     array(
        //                         "volume" => "0.500",
        //                         "price" => "0.10000000",
        //                         "fee" => "0.16431104",
        //                         "ctime" => 1510996571195,
        //                         "deal_price" => "0.10000000",
        //                         "id" => 306,
        //                         "type" => "买入"
        //                     }
        //                 ),
        //                 "status" => 3
        //             ),
        //             {
        //                 "side" => "SELL",
        //                 "total_price" => "0.10000000",
        //                 "created_at" => 1510993841000,
        //                 "avg_price" => "0.10000000",
        //                 "countCoin" => "btc",
        //                 "source" => 1,
        //                 "type" => 1,
        //                 "side_msg" => "买入",
        //                 "volume" => "1.000",
        //                 "price" => "0.10000000",
        //                 "source_msg" => "WEB",
        //                 "status_msg" => "未成交",
        //                 "deal_volume" => "0.00000000",
        //                 "id" => 425,
        //                 "remain_volume" => "0.00000000",
        //                 "baseCoin" => "eth",
        //                 "tradeList" => array(),
        //                 "status" => 1
        //             }
        //         )
        //     }
        // }
        $allOpenOrders = $this->filter_by_array($orderData, 'status', [0, 1, 3], false);
        return $this->parse_orders($allOpenOrders, $market, $since, $limit);
    }

    public function fetch_orders ($symbol = null, $since = null, $limit = 100, $params = array ()) {
        $this->load_markets();
        $openCloseOrders = array();
        if ($symbol === null) {
            $totalMarkets = is_array($this->markets) ? array_keys($this->markets) : array();
            for ($i = 0; $i < count($totalMarkets); $i++) {
                $market = $this->market ($totalMarkets[$i]);
                $orderData = $this->fetch_common_orders ($market['id'], $limit, $params);
                $parseOpenCloseOrderResult = $this->filter_by_array($orderData, 'status', [0, 1, 2, 3], false);
                $openCloseOrders = $this->array_concat($openCloseOrders, $parseOpenCloseOrderResult);
            }
            return $this->parse_orders($openCloseOrders, null, $since, $limit);
        }
        $market = $this->market ($symbol);
        $orderData = $this->fetch_common_orders ($market['id'], $limit, $params);
        $openCloseOrders = $this->filter_by_array($orderData, 'status', [1, 2, 3], false);
        return $this->parse_orders($openCloseOrders, $market, $since, $limit);
    }

    public function fetch_order ($id, $symbol = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' FetchOrder requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
            'time' => ($this->milliseconds ()),
            'order_id' => $id,
        );
        $response = $this->privateGetOpenApiOrderInfo (array_merge($request, $params));
        $result = $this->safe_value($response, 'data');
        return $this->parse_order($this->safe_value($result, 'order_info', array()), $market);
    }

    public function fetch_balance ($params = array ()) {
        $this->load_markets();
        $request = array(
            'time' => $this->milliseconds (),
        );
        $response = $this->privateGetOpenApiUserAccount (array_merge($request, $params));
        $result = array( 'info' => $response );
        $resultData = $this->safe_value($response, 'data');
        $balances = $this->safe_value($resultData, 'coin_list');
        for ($i = 0; $i < count($balances); $i++) {
            $balance = $balances[$i];
            $currencyId = $this->safe_string($balance, 'coin');
            $code = $this->safe_currency_code($currencyId);
            $account = array(
                'free' => $this->safe_float($balance, 'normal'),
                'used' => $this->safe_float($balance, 'locked'),
                // 'total' => $this->safe_float($balance, 'balance'),
            );
            $result[$code] = $account;
        }
        return $this->parse_balance($result);
    }

    public function handle_errors ($code, $reason, $url, $method, $headers, $body, $response, $requestHeaders, $requestBody) {
        if ($response === null) {
            return;
        }
        // EndPoints Result common pattern
        // {
        //     "$code" : "code_id",
        //     "msg" : "",
        //     "data" : array()
        // }
        $errorCode = $this->safe_string($response, 'code');
        if ($errorCode === '0') {
            // success
            return;
        }
        $errorMessages = $this->errorMessages;
        $message = null;
        $message = $this->safe_string($response, 'msg');
        if ($message === null) {
            $message = $this->safe_string($errorMessages, $errorCode, 'Unknown Error');
        }
        $feedback = $this->id . ' ' . $message;
        $this->throw_exactly_matched_exception($this->exceptions, $errorCode, $feedback);
        throw new ExchangeError($feedback);
    }
}
