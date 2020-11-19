<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import
use \ccxt\ExchangeError;
use \ccxt\InvalidOrder;

class aax extends Exchange {

    public function describe () {
        return array_replace_recursive(parent::describe (), array(
            'id' => 'aax',
            'name' => 'aax',
            'rateLimit' => 500,
            'has' => array(
                'fetchMarkets' => true,
                'fetchOHLCV' => true,
                'fetchOrderBook' => true,
                'fetchTrades' => true,
                'fetchBalance' => true,
                'createOrder' => true,
                'cancelOrder' => true,
                'fetchMyTrades' => true,
                'fetchOpenOrders' => true,
                'fetchOrders' => true,
                'fetchOrder' => true,
                'fetchTicker' => true,
            ),
            'timeframes' => array(
                '1m' => 1,
                '3m' => 3,
                '5m' => 5,
                '15m' => 15,
                '30m' => 30,
                '1h' => 60,
                '2h' => 120,
                '3h' => 180,
                '4h' => 240,
                '8h' => 480,
                '1d' => 1440,
            ),
            'headers' => array(
                'Content-Type' => 'application/json',
            ),
            'urls' => array(
                'api' => 'https://api.aax.com',
                'www' => 'https://www.aax.com/',
            ),
            'api' => array(
                'public' => array(
                    'get' => array(
                        'v2/instruments',
                        'v2/market/orderbook',
                        'marketdata/v1/getHistMarketData',
                        'v2/market/trades',
                        'v2/market/tickers',
                    ),
                ),
                'private' => array(
                    'get' => array(
                        'v2/account/balances',
                        'v2/spot/trades',
                        'v2/spot/openOrders',
                        'v2/spot/orders',
                        'v2/user/info',
                    ),
                    'post' => array(
                        'v2/spot/orders',
                    ),
                    'delete' => array(
                        'v2/spot/orders/cancel/{orderID}',
                    ),
                ),
            ),
            'exceptions' => array(
                '400' => '\\ccxt\\BadRequest',
                '401' => '\\ccxt\\AuthenticationError',
                '403' => '\\ccxt\\AuthenticationError',
                '429' => '\\ccxt\\PermissionDenied',
                '10003' => '\\ccxt\\BadRequest',
                '10006' => '\\ccxt\\AuthenticationError',
                '20001' => '\\ccxt\\InsufficientFunds',
                '20009' => '\\ccxt\\BadRequest',
                '30004' => '\\ccxt\\BadRequest',
                '30005' => '\\ccxt\\BadRequest',
                '30006' => '\\ccxt\\BadRequest',
                '30007' => '\\ccxt\\BadRequest',
                '30008' => '\\ccxt\\BadRequest',
                '30009' => '\\ccxt\\BadRequest',
                '30011' => '\\ccxt\\CancelPending',
                '30012' => '\\ccxt\\BadSymbol',
                '30013' => '\\ccxt\\BadSymbol',
                '30018' => '\\ccxt\\InvalidOrder',
                '30019' => '\\ccxt\\InvalidOrder',
                '30020' => '\\ccxt\\InvalidOrder',
                '30023' => '\\ccxt\\InvalidOrder',
                '30026' => '\\ccxt\\InvalidOrder',
                '30027' => '\\ccxt\\ExchangeError',
                '30030' => '\\ccxt\\InvalidOrder',
                '30047' => '\\ccxt\\InvalidOrder',
            ),
            'errorMessages' => array(
                '400' => 'There is something wrong with your request',
                '401' => 'Your API key is wrong',
                '403' => 'Your API key does not have enough privileges to access this resource',
                '429' => 'You have exceeded your API key rate limits',
                '500' => 'Internal Server Error',
                '503' => 'Service is down for maintenance',
                '504' => 'Request timeout expired',
                '550' => 'You requested data that are not available at this moment',
                '10003' => 'Parameter validation error',
                '10006' => 'Session expired, please relogin',
                '20001' => 'Insufficient balance. Please deposit to trade',
                '20009' => 'Order amount must be positive',
                '30004' => 'Minimum quantity is {0}',
                '30005' => 'Quantity maximum precision is {0} decimal places',
                '30006' => 'Price maximum precision is {0} decimal places',
                '30007' => 'Minimum price is {0}',
                '30008' => 'Stop price maximum precision is {0} decimal places',
                '30009' => 'Stop Price cannot be less than {0}',
                '30011' => 'The order is being cancelled, please wait',
                '30012' => 'Unknown currency',
                '30013' => 'Unknown symbol',
                '30018' => 'Order price cannot be greater than {0}',
                '30019' => 'Order quantity cannot be greater than {0}',
                '30020' => 'Order price must be a multiple of {0}',
                '30023' => 'Order failed, please try again',
                '30026' => 'Quantity is not a multiple of {0}',
                '30027' => 'Close position failed, it is recommended that you cancel the current order and then close the position',
                '30028' => 'Symbol cannot be traded at this time',
                '30030' => 'Price cannot be specified for market orders',
                '30037' => 'Once stop limit order triggered, stop price cannot be amended',
                '30040' => 'Order status has changed, please try again later',
                '30047' => 'The order is closed. Can nott cancel',
                '30049' => 'The order is being modified, please wait',
                '40009' => 'Too many requests',
                '50001' => 'Server side exception, please try again later',
                '50002' => 'Server is busy, please try again later',
            ),
        ));
    }

    public function sign ($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $url = $this->urls['api'];
        $queryParams = '/' . $this->implode_params($path, $params);
        $query = $this->omit ($params, $this->extract_params($path));
        if ($api === 'public' || $method === 'GET') {
            if ($query) {
                $queryParams .= '?' . $this->urlencode ($query);
            }
        }
        if ($api === 'private') {
            $nonce = (string) $this->milliseconds ();
            $signature = $nonce . ':' . $method . $queryParams;
            if ($method !== 'GET' && $method !== 'HEAD') {
                $body = $this->json ($query);
                $signature .= $body;
            }
            $encodedHEX = $this->hmac ($this->encode ($signature), $this->encode ($this->secret), 'sha256');
            $headers = array(
                'X-ACCESS-KEY' => $this->apiKey,
                'X-ACCESS-NONCE' => $nonce,
                'X-ACCESS-SIGN' => $encodedHEX,
            );
        }
        $url .= $queryParams;
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function fetch_markets ($params = array ()) {
        $response = $this->publicGetV2Instruments ();
        // Exchange Response
        // {
        //     "$code":1,
        //     "data":array(
        //        array(
        //           "tickSize":"0.1",
        //           "lotSize":"0.0001",
        //           "$base":"BTC",
        //           "$quote":"USDT",
        //           "minQuantity":"0.0010000000",
        //           "maxQuantity":"999900.0000000000",
        //           "minPrice":"0.1000000000",
        //           "maxPrice":"10000000.0000000000",
        //           "$status":"enable",
        //           "$symbol":"BTCUSDT",
        //           "$code":null,
        //           "takerFee":"0.00000",
        //           "makerFee":"0.00000",
        //           "multiplier":"1.000000000000",
        //           "mmRate":"0.02500",
        //           "imRate":"0.05000",
        //           "type":"spot"
        //        ),
        //        ...
        //     ),
        //     "message":"success",
        //     "ts":1573561743499
        //  }
        $result = array();
        $markets = $this->safe_value($response, 'data');
        for ($i = 0; $i < count($markets); $i++) {
            $market = $markets[$i];
            $code = $this->safe_string($market, 'code');
            if (($code && strtoupper($code) === 'FP')) {
                continue;
            }
            $id = $this->safe_string($market, 'symbol');
            $baseId = $this->safe_string($market, 'base');
            $quoteId = $this->safe_string($market, 'quote');
            $base = $this->safe_currency_code($baseId);
            $quote = $this->safe_currency_code($quoteId);
            $symbol = $baseId . '/' . $quoteId;
            $status = $this->safe_string($market, 'status');
            $active = null;
            if ($status !== null) {
                $active = (strtoupper($status) === 'ENABLE');
            }
            $precision = array(
                'price' => $this->precision_from_string($market['tickSize']),
                'amount' => $this->precision_from_string($market['lotSize']),
            );
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
                'type' => $this->safe_string($market, 'type'),
                'taker' => $this->safe_float($market, 'takerFee'),
                'maker' => $this->safe_float($market, 'makerFee'),
                'limits' => array(
                    'amount' => array(
                        'min' => $this->safe_float($market, 'minQuantity'),
                        'max' => $this->safe_float($market, 'maxQuantity'),
                    ),
                    'price' => array(
                        'min' => $this->safe_float($market, 'minPrice'),
                        'max' => $this->safe_float($market, 'maxPrice'),
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

    public function fetch_ohlcv ($symbol = 'BTC/USDT', $timeframe = '1m', $since = null, $limit = 30, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'date_scale' => $this->timeframes[$timeframe],
            'base' => $market['base'],
            'quote' => $market['quote'],
            'limit' => $limit,
        );
        if ($since !== null) {
            $request['from'] = $since;
        }
        if (is_array($params) && array_key_exists('to', $params)) {
            $request['to'] = $params['to'];
        }
        $response = $this->publicGetMarketdataV1GetHistMarketData (array_merge($request, $params));
        $result = array();
        if (is_array($response && $response['s'] === 'ok') && array_key_exists('s', $response && $response['s'] === 'ok')) {
            $timeArr = $response['t'];
            $openArr = $response['o'];
            $highArr = $response['h'];
            $lowArr = $response['l'];
            $closeArr = $response['c'];
            $volumeArr = $response['v'];
            $prevOpenTime = null;
            for ($i = 0; $i < count($timeArr); $i++) {
                $openTime = (intval ($timeArr[$i]) * 1000);
                if ($openTime !== $prevOpenTime) {
                    $ohlcvArr = array();
                    $ohlcvArr[] = $openTime;
                    $ohlcvArr[] = $openArr[$i];
                    $ohlcvArr[] = $highArr[$i];
                    $ohlcvArr[] = $lowArr[$i];
                    $ohlcvArr[] = $closeArr[$i];
                    $ohlcvArr[] = $volumeArr[$i] / $closeArr[$i];
                    $result[] = $ohlcvArr;
                    $prevOpenTime = $openTime;
                }
            }
        }
        return $this->parse_ohlcvs($result, $market, $timeframe, $since, $limit);
    }

    public function parse_ticker ($ticker, $market = null, $time = null) {
        $symbol = null;
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        $timestamp = $time;
        $open = $this->safe_float($ticker, 'o');
        $last = $this->safe_float($ticker, 'c');
        $change = null;
        $percentage = null;
        $average = null;
        if ($last !== null && $open !== null) {
            $change = $last - $open;
            $average = $this->sum ($last, $open) / 2;
            if ($open > 0) {
                $percentage = $change / $open * 100;
            }
        }
        return array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'high' => $this->safe_float($ticker, 'h'),
            'low' => $this->safe_float($ticker, 'l'),
            'bid' => null,
            'bidVolume' => null,
            'ask' => null,
            'askVolume' => null,
            'vwap' => null,
            'open' => $open,
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => $change,
            'percentage' => $percentage,
            'average' => $average,
            'baseVolume' => null,
            'quoteVolume' => $this->safe_float($ticker, 'v'),
            'info' => $ticker,
        );
    }

    public function fetch_ticker ($symbol, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $response = $this->publicGetV2MarketTickers (array_merge($params));
        $result = $this->safe_value($response, 'tickers', array());
        $pair = $market['id'];
        for ($i = 0; $i < count($result); $i++) {
            $ticker = $result[$i];
            if ($pair === $ticker['s']) {
                return $this->parse_ticker($ticker, $market, $this->safe_integer($response, 't'));
            }
        }
        return null;
    }

    public function fetch_order_book ($symbol = 'BTC/USDT', $limit = 50, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
            'level' => $limit,
        );
        $response = $this->publicGetV2MarketOrderbook (array_merge($request, $params));
        // Response Format
        // {
        //     "asks":array(
        //        array(
        //           "10823.00000000", #price
        //           "0.004000"  #size
        //        ),
        //        array(
        //           "10823.10000000",
        //           "0.100000"
        //        ),
        //        array(
        //           "10823.20000000",
        //           "0.010000"
        //        )
        //     ),
        //     "bids":array(
        //        array(
        //           "10821.20000000",
        //           "0.002000"
        //        ),
        //        array(
        //           "10821.10000000",
        //           "0.005000"
        //        ),
        //        array(
        //           "10820.40000000",
        //           "0.013000"
        //        )
        //     ),
        //     "e":"BTCUSDT@book_50",
        //     "t":1561543614756
        //  }
        $timestamp = $this->safe_integer($response, (string) 't');
        return $this->parse_order_book($response, $timestamp);
    }

    public function parse_trade ($trade, $market = null) {
        // From FetchTrades
        //   {
        //     "e":"BTCUSDFP@trades",
        //     "trades":
        //         [ array( "p":"9395.50000000",
        //            "q":"50.000000",
        //            "t":1592563996718
        //          ),
        //         array(  "p":"9395.50000000",
        //            "q":"50.000000",
        //            "t":1592563993577
        //         )]
        //   }
        // Response From FetchMyTrdaes
        // {
        //        array(
        //           {
        //              "avgPrice":"8000",
        //              "$base":"BTC",
        //              "commission":"0.00000888",
        //              "createTime":"2019-11-12T03:18:35Z",
        //              "cumQty":"0.0148",
        //              "filledPrice":"8000",
        //              "filledQty":"0.0148",
        //              "leavesQty":"0.0052",
        //              "orderID":"wFo9ZPxAJ",
        //              "orderQty":"0.02",
        //              "orderStatus":2,
        //              "orderType":2,
        //              "$price":"8000",
        //              "$quote":"USDT",
        //              "rejectCode":0,
        //              "rejectReason":null,
        //              "$side":1,
        //              "stopPrice":"0",
        //              "$symbol":"BTCUSDT",
        //              "taker":false,
        //              "transactTime":"2019-11-12T03:16:16Z",
        //              "updateTime":null,
        //              "userID":"216214"
        //           }
        //        ),
        //  }
        $timestamp = $this->safe_string($trade, 't');
        if ($timestamp === null) {
            $timestamp = $this->safe_string($trade, 'createTime');
            if ($timestamp !== null) {
                $timestamp = $this->parse8601 ($timestamp);
            }
        }
        $symbol = null;
        if ($market !== null) {
            $symbol = $this->safe_string($market, 'symbol');
        }
        if ($symbol === null) {
            $base = $this->safe_string($trade, 'base');
            $quote = $this->safe_string($trade, 'quote');
            if ($base !== null && $quote !== null) {
                $symbol = $base . '/' . $quote;
            }
        }
        $price = $this->safe_float_2($trade, 'p', 'avgPrice');
        $amount = $this->safe_float_2($trade, 'q', 'orderQty');
        $sideType = $this->safe_integer($trade, 'side');
        $side = null;
        if ($sideType !== null) {
            if ($sideType === 1) {
                $side = 'BUY';
            }
            if ($sideType === 2) {
                $side = 'SELL';
            }
        }
        if ($side === null) {
            if ($price < 0) {
                $side = 'SELL';
            } else {
                $side = 'BUY';
            }
            $price = abs($price);
        }
        $cost = null;
        if ($price !== null && $amount !== null && $symbol !== null) {
            $cost = floatval ($this->cost_to_precision($symbol, $price * $amount));
        }
        $takerOrMaker = null;
        if (is_array($trade) && array_key_exists('taker', $trade)) {
            $takerOrMaker = $trade['taker'] ? 'taker' : 'maker';
        }
        $orderId = $this->safe_string($trade, 'orderID');
        return array(
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'symbol' => $symbol,
            'id' => $orderId,
            'order' => $orderId,
            'type' => null,
            'side' => $side,
            'takerOrMaker' => $takerOrMaker,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'fee' => $this->safe_string($trade, 'commission'),
        );
    }

    public function fetch_trades ($symbol, $since = null, $limit = 2000, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'symbol' => $market['id'],
            'limit' => $limit,
        );
        $response = $this->publicGetV2MarketTrades (array_merge($request, $params));
        // Response Received
        // {
        //     "e":"BTCUSDFP@trades",
        //     "trades":
        //         [ array( "p":"9395.50000000",
        //            "q":"50.000000",
        //            "t":1592563996718
        //          ),
        //         array(  "p":"9395.50000000",
        //            "q":"50.000000",
        //            "t":1592563993577
        //         )]
        //   }
        return $this->parse_trades($this->safe_value($response, 'trades'), $market, $since, $limit);
    }

    public function fetch_balance ($params = array ()) {
        $request = array(
            'purseType' => 'SPTP', // spot only for now
        );
        $response = $this->privateGetV2AccountBalances (array_merge($request, $params));
        // FetchBalance Response
        //    {
        //      "$code":1,
        //      "data":array(
        //      array(
        //        "purseType":"FUTP",
        //        "currency":"BTC",
        //        "available":"0.41000000",
        //        "unavailable":"0.00000000"
        //      ),
        //      {
        //        "purseType":"FUTP",
        //        "currency":"USDT",
        //        "available":"0.21000000",
        //        "unvaliable":"0.00000000"
        //      }
        //    )
        //      "message":"success",
        //      "ts":1573530401020
        //    }
        $result = array( 'info' => $response );
        $balances = $this->safe_value($response, 'data');
        for ($i = 0; $i < count($balances); $i++) {
            $balance = $balances[$i];
            $currencyId = $this->safe_string($balance, 'currency');
            $code = $this->safe_currency_code($currencyId);
            $account = array(
                'free' => $this->safe_float($balance, 'available'),
                'used' => $this->safe_float($balance, 'unavailable'),
            );
            $result[$code] = $account;
        }
        return $this->parse_balance($result);
    }

    public function parse_order_type ($type) {
        $orderTypes = array(
            '1' => 'market',
            '2' => 'limit',
            '3' => 'stop',
            '4' => 'stop-limit',
        );
        return $this->safe_string($orderTypes, $type, $type);
    }

    public function parse_order_status ($status) {
        $statuses = array(
            '0' => 'open', // pending-new
            '1' => 'open', // new
            '2' => 'open', // partiallyfilled
            '3' => 'closed', // filled
            '4' => 'canceled', // cancel - rejected
            '5' => 'canceled', // canceled
            '6' => 'rejected', // rejected
            '10' => 'canceled', // canceled
            '11' => 'rejected', // business-rejct
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_order ($order, $market = null, $time = null) {
        // CraeteOrder,cancelOrder Response
        //       array(
        //        "avgPrice":"0",
        //        "$base":"BTC",
        //        "clOrdID":"aax",
        //        "commission":"0",
        //        "createTime":null,
        //        "cumQty":"0",
        //        "id":null,
        //        "isTriggered":null,
        //        "lastPrice":"0",
        //        "lastQty":"0",
        //        "leavesQty":"0",
        //        "orderID":"wJ4L366KB",
        //        "orderQty":"0.02",
        //        "orderStatus":0,
        //        "$orderType":2,
        //        "$price":"8000",
        //        "$quote":"USDT",
        //        "rejectCode":null,
        //        "rejectReason":null,
        //        "$side":1,
        //        "stopPrice":null,
        //        "$symbol":"BTCUSDT",
        //        "transactTime":null,
        //        "updateTime":null,
        //        "timeInForce":1,
        //        "userID":"216214"
        //     ),
        $timestamp = $this->safe_string($order, 'createTime');
        if ($timestamp === null && $time !== null) {
            $timestamp = $time;
        } else {
            if (strlen($timestamp) !== 13) {
                $timestamp = $this->parse8601 ($timestamp);
            } else {
                $timestamp = intval ($timestamp);
            }
        }
        $price = $this->safe_float($order, 'price');
        $amount = $this->safe_float($order, 'orderQty');
        $cost = null;
        $symbol = null;
        if ($market !== null) {
            $symbol = $this->safe_string($market, 'symbol');
        }
        if ($symbol === null) {
            $base = $this->safe_string($order, 'base');
            $quote = $this->safe_string($order, 'quote');
            if ($base !== null && $quote !== null) {
                $symbol = $base . '/' . $quote;
            }
        }
        if ($price !== null && $amount !== null && $symbol !== null) {
            $cost = floatval ($this->cost_to_precision($symbol, $price * $amount));
        }
        $sideType = $this->safe_integer($order, 'side');
        $side = null;
        if ($sideType !== null) {
            if ($sideType === 1) {
                $side = 'BUY';
            }
            if ($sideType === 2) {
                $side = 'SELL';
            }
        }
        $remaining = $this->safe_float($order, 'leavesQty');
        $filled = null;
        if ($remaining !== null && $amount !== null) {
            $filled = $amount - $remaining;
        }
        $orderType = $this->parse_order_type ($this->safe_string($order, 'orderType'));
        $status = $this->parse_order_status($this->safe_string($order, 'orderStatus'));
        return array(
            'info' => $order,
            'id' => $this->safe_string($order, 'orderID'),
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'lastTradeTimestamp' => null,
            'symbol' => $symbol,
            'type' => $orderType,
            'side' => $side,
            'price' => $price,
            'stop_price' => $this->safe_string($order, 'stopPrice'),
            'amount' => $amount,
            'cost' => $cost,
            'average' => $this->safe_float($order, 'avgPrice'),
            'filled' => $filled,
            'remaining' => $remaining,
            'status' => $status,
            'fee' => $this->safe_string($order, 'commission'),
            'trades' => null,
        );
    }

    public function create_order ($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $type = strtoupper($type);
        if ($type === 'STOP_LIMIT') {
            $type = 'STOP-LIMIT';
        }
        $request = array(
            // === Required ===
            // orderType : string // can be MARKET,LIMIT,STOP,STOP-LIMIT
            // $symbol : string
            // orderQty : string // Buying or selling quantity
            // $side : string // BUY or SELL
            // === Required according to ordeType ===
            // $price : string // limit $price in limit and stop-limit orders
            // $stopPrice : string // Trigger $price for stop-limit order and stop order
            // === Optional ===
            // clOrdID : string
            // timeInForce :string // GTC/IOC/FOK，default is GTC
            'orderType' => $type,
            'symbol' => $market['id'],
            'orderQty' => $this->amount_to_precision($symbol, $amount),
            'side' => strtoupper($side),
            'clOrdID' => 'quadency',
        );
        if (($type === 'LIMIT') || ($type === 'STOP-LIMIT')) {
            if ($price === null) {
                throw new InvalidOrder($this->id . ' createOrder method requires a $price for a ' . $type . ' order');
            }
            $request['price'] = $this->price_to_precision($symbol, $price);
        }
        if (($type === 'STOP') || ($type === 'STOP-LIMIT')) {
            $stopPrice = $this->safe_float($params, 'stopPrice');
            if ($stopPrice === null) {
                throw new InvalidOrder($this->id . ' createOrder method requires a $stopPrice extra param for a ' . $type . ' order');
            }
            $request['stopPrice'] = $this->price_to_precision($symbol, $stopPrice);
        }
        $response = $this->privatePostV2SpotOrders (array_merge($request, $params));
        // Response
        // {
        //     "code":1,
        //     "data":array(
        //        "avgPrice":"0",
        //        "base":"BTC",
        //        "clOrdID":"aax",
        //        "commission":"0",
        //        "createTime":null,
        //        "cumQty":"0",
        //        "id":null,
        //        "isTriggered":null,
        //        "lastPrice":"0",
        //        "lastQty":"0",
        //        "leavesQty":"0",
        //        "orderID":"wJ4L366KB",
        //        "orderQty":"0.02",
        //        "orderStatus":0,
        //        "orderType":2,
        //        "$price":"8000",
        //        "quote":"USDT",
        //        "rejectCode":null,
        //        "rejectReason":null,
        //        "$side":1,
        //        "$stopPrice":null,
        //        "$symbol":"BTCUSDT",
        //        "transactTime":null,
        //        "updateTime":null,
        //        "timeInForce":1,
        //        "userID":"216214"
        //     ),
        //     "message":"success",
        //     "ts":1573530401264
        //  }
        return $this->parse_order($this->safe_value($response, 'data'), $market, $this->safe_string($response, 'ts'));
    }

    public function cancel_order ($id, $symbol = null, $params = array ()) {
        $this->load_markets();
        $market = null;
        if ($symbol !== null) {
            $this->load_markets();
            $market = $this->market ($symbol);
        }
        $request = array(
            'orderID' => $id,
        );
        $response = $this->privateDeleteV2SpotOrdersCancelOrderID (array_merge($request, $params));
        // Response
        // {
        //     "code":1,
        //     "data":array(
        //        "avgPrice":"0",
        //        "base":"BTC",
        //        "clOrdID":"aax",
        //        "commission":"0",
        //        "createTime":"2019-11-12T03:46:41Z",
        //        "cumQty":"0",
        //        "$id":"114330021504606208",
        //        "isTriggered":false,
        //        "lastPrice":"0",
        //        "lastQty":"0",
        //        "leavesQty":"0",
        //        "orderID":"wJ4L366KB",
        //        "orderQty":"0.05",
        //        "orderStatus":1,
        //        "orderType":2,
        //        "price":"8000",
        //        "quote":"USDT",
        //        "rejectCode":0,
        //        "rejectReason":null,
        //        "side":1,
        //        "stopPrice":"0",
        //        "$symbol":"BTCUSDT",
        //        "transactTime":null,
        //        "updateTime":"2019-11-12T03:46:41Z",
        //        "timeInForce":1,
        //        "userID":"216214"
        //     ),
        //     "message":"success",
        //     "ts":1573530402029
        //  }
        return $this->parse_order($this->safe_value($response, 'data'), $market, $this->safe_string($response, 'ts'));
    }

    public function fetch_my_trades ($symbol = null, $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $request = array(
            // pageNum : Integer // optional
            // pageSize : Integer // optional
            // base : String // optional
            // quote : String // optional
            // orderId : String //optional
            // startDate : String //optional
            // endDate : String //optional
            // side : String // optional
            // orderType : String // optional
        );
        $market = null;
        if ($symbol !== null) {
            $market = $this->market ($symbol);
            $request['base'] = $market['baseId'];
            $request['quote'] = $market['quoteId'];
        }
        if ($since !== null) {
            $request['startDate'] = $this->ymd ($since, '-');
        }
        if ($limit !== null) {
            $request['pageSize'] = $limit;
        }
        $response = $this->privateGetV2SpotTrades (array_merge($request, $params));
        // Response
        // {
        //     "code":1,
        //     "data":{
        //        "list":array(
        //           array(
        //              "avgPrice":"8000",
        //              "base":"BTC",
        //              "commission":"0.00000888",
        //              "createTime":"2019-11-12T03:18:35Z",
        //              "cumQty":"0.0148",
        //              "filledPrice":"8000",
        //              "filledQty":"0.0148",
        //              "id":"114322949580906499",
        //              "leavesQty":"0.0052",
        //              "orderID":"wFo9ZPxAJ",
        //              "orderQty":"0.02",
        //              "orderStatus":2,
        //              "orderType":2,
        //              "price":"8000",
        //              "quote":"USDT",
        //              "rejectCode":0,
        //              "rejectReason":null,
        //              "side":1,
        //              "stopPrice":"0",
        //              "$symbol":"BTCUSDT",
        //              "taker":false,
        //              "transactTime":"2019-11-12T03:16:16Z",
        //              "updateTime":null,
        //              "userID":"216214"
        //           }
        //        ),
        //        "pageNum":1,
        //        "pageSize":1,
        //        "total":10
        //     ),
        //     "message":"success",
        //     "ts":1573532934832
        //  }
        $result = $this->safe_value($response, 'data');
        return $this->parse_trades($this->safe_value($result, 'list', array()), $market, $since, $limit);
    }

    public function fetch_open_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $request = array(
            // pageNum : Integer // optional
            // pageSize : Integer // optional
            // $symbol : String // optional
            // orderId : String // optional
            // side : String // optional
            // orderType : String // optional
            // clOrdID : String //optional
        );
        $market = null;
        if ($symbol !== null) {
            $market = $this->market ($symbol);
            $request['symbol'] = $market['id'];
        }
        if ($limit !== null) {
            $request['pageSize'] = $limit;
        }
        $response = $this->privateGetV2SpotOpenOrders (array_merge($request, $params));
        // Response
        // {
        //     "code":1,
        //     "data":array(
        //        "list":array(
        //           array(
        //              "avgPrice":"0",
        //              "base":"BTC",
        //              "clOrdID":"aax",
        //              "commission":"0",
        //              "createTime":"2019-11-12T03:41:52Z",
        //              "cumQty":"0",
        //              "id":"114328808516083712",
        //              "isTriggered":false,
        //              "lastPrice":"0",
        //              "lastQty":"0",
        //              "leavesQty":"0",
        //              "orderID":"wJ3qitASB",
        //              "orderQty":"0.02",
        //              "orderStatus":1,
        //              "orderType":2,
        //              "price":"8000",
        //              "quote":"USDT",
        //              "rejectCode":0,
        //              "rejectReason":null,
        //              "side":1,
        //              "stopPrice":"0",
        //              "$symbol":"BTCUSDT",
        //              "transactTime":null,
        //              "updateTime":"2019-11-12T03:41:52Z",
        //              "timeInForce":1,
        //              "userID":"216214"
        //           ),
        //           ...
        //        ),
        //        "pageNum":1,
        //        "pageSize":2,
        //        "total":2
        //     ),
        //     "message":"success",
        //     "ts":1573553718212
        //  }
        $result = $this->safe_value($response, 'data');
        return $this->parse_orders($this->safe_value($result, 'list', array()), $market, $since, $limit);
    }

    public function fetch_orders ($symbol = null, $since = null, $limit = 100, $params = array ()) {
        $this->load_markets();
        $request = array(
            // pageNum : Integer // optional
            // pageSize : Integer // optional
            // $symbol : String // optional
            // orderId : String // optional
            // side : String // optional
            // orderType : String // optional
            // clOrdID : String //optional
            // base : string // optional
            // quote :string // optional
            // orderStatus : Integer //optional 1 => new, 2:filled, 3:cancel
        );
        $market = null;
        if ($symbol !== null) {
            $market = $this->market ($symbol);
            $request['base'] = $market['baseId'];
            $request['quote'] = $market['quoteId'];
        }
        if ($limit !== null) {
            $request['pageSize'] = $limit;
        }
        $response = $this->privateGetV2SpotOrders (array_merge($request, $params));
        $result = $this->safe_value($response, 'data');
        return $this->parse_orders($this->safe_value($result, 'list', array()), $market, $since, $limit);
    }

    public function fetch_order ($id, $symbol = null, $params = array ()) {
        $this->load_markets();
        $request = array(
            'orderID' => $id,
        );
        $response = $this->privateGetV2SpotOrders (array_merge($request, $params));
        $result = $this->safe_value($response, 'data');
        $list = $this->safe_value($result, 'list', array());
        return $this->parse_order($list[0]);
    }

    public function fetch_user_id () {
        $response = $this->privateGetV2UserInfo ();
        $result = $this->safe_value($response, 'data');
        return $this->safe_value($result, 'userID');
    }

    public function handle_errors ($code, $reason, $url, $method, $headers, $body, $response, $requestHeaders, $requestBody) {
        if ($response === null) {
            return;
        }
        $errorCode = $this->safe_string($response, 'code');
        if ($errorCode === null) {
            // fetchOrderBook or fetchTrades or fetchOhlcv
            return;
        }
        if ($errorCode === '1') {
            // success
            return;
        }
        $errorMessages = $this->errorMessages;
        $message = null;
        $message = $this->safe_string($response, 'message');
        if ($message === null) {
            $message = $this->safe_string($errorMessages, $errorCode, 'Unknown Error');
        }
        $feedback = $this->id . ' ' . $message;
        $this->throw_exactly_matched_exception($this->exceptions, $errorCode, $feedback);
        throw new ExchangeError($feedback);
    }
}
