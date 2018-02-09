#!/usr/bin/env python3
# Bittrex CLI Tool
# Darkerego 2018


""" Imports """ 
import bittrex
import sys
import json
import argparse
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename='bittrextool.log')

#TODO: map out the ret of these funtions

"""
    Bittrex API Lib Functions
 |  
 |  buylimit(self, market, quantity, rate)
 |  
 |  buymarket(self, market, quantity)
 |  
 |  cancel(self, uuid)
 |  
 |  getbalance(self, currency)
 |  
 |  getbalances(self)
 |  
 |  getcurrencies(self)
 |  
 |  getdepositaddress(self, currency)
 |  
 |  getdeposithistory(self, currency, count)
 |  
 |  getmarkethistory(self, market, count=20)
 |  
 |  getmarkets(self)
 |  
 |  getmarketsummaries(self)
 |  
 |  getmarketsummary(self, market)
 |  
 |  getopenorders(self, market)
 |  
 |  getorder(self, uuid)
 |  
 |  getorderbook(self, market, type, depth=20)
 |  
 |  getorderhistory(self, market, count)
 |  
 |  getticker(self, market)
 |  
 |  getwithdrawalhistory(self, currency, count)
 |  query(self, method, values={})
 |  
 |  selllimit(self, market, quantity, rate)
 |  
 |  sellmarket(self, market, quantity)
 |  
 |  withdraw(self, currency, quantity, address)


"""

# some globals
key = ''
secret = ''
withdrawal_enabled=True

# return time
def timeStamp():
     return time.time()

 # print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



# legacy config file stuff
try:
    # For Python 3+
    from configparser import ConfigParser, NoSectionError
except ImportError:
    # Fallback to Python 2.7
    from ConfigParser import ConfigParser, NoSectionError
def main(argv):
    # Setup Argument Parser
    parser = argparse.ArgumentParser(description='Python3 Bittrex API Tool')
    # functions
    parser.add_argument('-f', '--config', default='./bittrex.cfg', type=str, required=False, help='config .cfg file')
    parser.add_argument('-t', '--ticker', default=False, action='store_true', required=False, help='Get ticker information for pai , specify with -p (example: BTC-ETH)')
    parser.add_argument('-d', '--deposit_address', action='store_true', default=False, required=False, help='Get deposit addresses for currency (specify with -c)')
    parser.add_argument('-D', '--debug', action='store_true', default=False, required=False, help='Enable extra verbose messages for debugging')
    parser.add_argument('-B', '--balances', default=False, action='store_true', required=False, help='Get all available balances')
    parser.add_argument('-k', '--balance', default=False, action='store_true', required=False, help='Get a particular account balance (specifiy with -c)')
    parser.add_argument('-b', '--buy_limit', default=False, action='store_true', required=False, help='Buy Limit Order ')
    parser.add_argument('-s', '--sell_limit', default=False, action='store_true', required=False, help='Sell Limit Order')
    parser.add_argument('-C', '--cancel_order', default=False, action='store_true' ,required=False, help="Cancel an order")
    parser.add_argument('-W', '--withdraw', default=False, action='store_true', required=False, help="DANGEROUS: Withdraw (specify currency <-c>, amount <-a>, and address <-A>)")
    parser.add_argument('-w', '--withdrawal_history', default=False, action='store_true', required=False, help='Get withdrawl history (specify currency <-c> , and optionally count <-x>) ')
    
    # arguments to functions
    #str
    
    parser.add_argument('-c', '--currency', default='null', type=str, required=False, help='Specify a currency (example: BTC)')
    parser.add_argument('-p', '--pair', default='null', type=str, required=False, help='Specify a currency pair (example: BTC_ETH)')
    parser.add_argument('-i', '--order_id', type=str, default='null',required=False, help="Specify an order id")
    parser.add_argument('-A', '--address', type=str, default='null', required=False, help="Specify a crypto wallet address for withdrawal (example: 15isHXhXV85i7QFwwwed9gg9ET5mWjNppP")
    
    # int
    parser.add_argument('-x', '--count', default=10, type=int, required=False, help='Specify a count <for histories>')
    #float
    parser.add_argument('-a', '--amount', default='0.0', type=float, required=False, help='Specify an amount to buy, sell, withdraw, etc')
    parser.add_argument('-P', '--price', default='0.0', type=float , required=False, help="Price to buy or sell at")
     
    # parse args
    args = parser.parse_args()
    config = ConfigParser()
    debug = args.debug
    ticker = args.ticker
    deposit_address = args.deposit_address
    balances = args.balances
    balance = args.balance
    buy_limit = args.buy_limit
    sell_limit = args.sell_limit
    cancel_order = args.cancel_order
    withdraw = args.withdraw
    withdrawal_history = args.withdrawal_history
    address = args.address
    
    
    currency = args.currency
    pair = args.pair
    order_id = args.order_id
    count = args.count
    amount = args.amount
    price = args.price

    # read config
    try:
        config.read(args.config)
        bittrexKey = config.get('keys', 'bittrexKey')
        bittrexSecret = config.get('keys', 'bittrexSecret')
        key = bittrexKey
        secret = bittrexSecret
        if debug: print("%s : %s" % (key,secret))
    except NoSectionError:
        print('No Config File Found! Running in Drymode!')
        args.dryrun = True
        poloniexkey = 'BITTREX_API_KEY'
        poloniexsecret = 'BITTREX_API_SECRET'
        config.set('keys', 'bittrexKey', bittrexkey)
        config.set('keys', 'bittrexSecret', bittrexsecret)

        try:
            with open(args.config, 'w') as configfile:
                config.write(configfile)
        except IOError:
            eprint('Failed to create and/or write to {}'.format(args.config))
        # do stuff here
        api = bittrex.bittrex(key, secret)
        # Start Program
        tS = timeStamp()
        logging.debug("Program started at %s" % tS)
        # API functions
    def get_ticker(pair):
        api = bittrex.bittrex(key, secret)
        if pair == 'null':
            eprint('WARN: No pair specified, defaulting to BTC-ETH')
            pair == 'BTC-ETH'
        try:
            t = api.getticker(pair)
        except Exception as err:
            logging.error(err)
            eprint('Error getting ticker data: '+str(err))
            return False
        else:
            tt = json.dumps(t)
            return(tt)
        
    def get_deposit_address(currency):
        api = bittrex.bittrex(key, secret)
        if currency == 'null':
            eprint('WARN: No currency specified, defaulting to BTC')
            currency = 'BTC'
        try:
            add = api.getdepositaddress(currency)
        except Exception as err:
            logging.error(err)
            eprint("Error getting deposit address: "+ str(err))
            return False
        else:
            add_ = json.dumps(add)
            return add_
        
    def get_balances():
        
        api = bittrex.bittrex(key, secret)
        try:
            bals = api.getbalances()
        except Exception as err:
            logging.error(err)
            eprint('Error getting balances' + str(err))
            return False
        else:
            bals = json.dumps(bals)
            return bals
        
    def get_balance(currency):
        api = bittrex.bittrex(key, secret)
        if currency == 'null':
            eprint('WARN: No currency specified, defaulting to BTC')
            currency = 'BTC'
        try:
            bal = api.getbalance(currency)
        except Exception as err:
            logging.info(err)
            eprint('Error getting balance' + str(err))
            return False
        else:
            bal = json.dumps(bal)
            return bal
        
    def buy_limit_order(pair, amount, price):
        api = bittrex.bittrex(key, secret)
        if pair == 'null':
            eprint('Specify a pair with -p')
            return False
        if amount == '0.0':
            eprint('Specify an amount with -a')
            return False
        if price == '0.0':
            eprint('Specify a price with -P')
            return False
        try:
            ret = api.buylimit(pair, amount, price)
        except Exception as err:
            logging.info(err)
            eprint('Error placing buy limit order: '+ str(err))
            return False
        else:
            ret = json.dumps(ret)
            return(ret)

    def sell_limit_order(pair, amount, price):
        api = bittrex.bittrex(key, secret)
        if pair == 'null':
            eprint('Specify a pair with -p')
            return False
        if amount == '0.0':
            eprint('Specify an amount with -a')
            return False
        if price == '0.0':
            eprint('Specify a price with -P')
            return False
        try:
            ret = api.selllimit(pair, amount, price)
        except Exception as err:
            logging.info(err)
            eprint('Error placing sell limit order: '+ str(err))
            return False
        else:
            ret = json.dumps(ret)
            return(ret)

    def cancel(order_id):
        api = bittrex.bittrex(key, secret)
        if order_id == 'null':
            eprint('Specify an order_id with -i')
            return False
        try:
            ret = api.cancel(order_id)
        except Exception as err:
            logging.info(err)
            eprint('Error canceling order: '+ str(err))
            return False
        else:
            ret = json.dumps(ret)
            return(ret)

    def do_withdraw(currency, amount, address):
        api = bittrex.bittrex(key, secret)
        if currency == 'null':
            eprint('Specify a currency with -c !')
            return False
        if amount == '0.0':
            eprint('Specify an amount with -a !')
            return False
        if address == 'null':
            eprint('Specify an address with -A !')
            return False
        try:
            ret = api.withdraw(currency, amount, address)
        except Exception as err:
            logging.error(err)
            eprint('Error withdrawing currency: ' + str(err))
            return False
        else:
            ret = json.dumps(ret)
            return(ret)
        
    def wd_history(currency, count=10):
        api = bittrex.bittrex(key, secret)
        if currency == 'null':
            eprint('No currency specified, defaulting to BTC')
            currency = 'BTC'
        try:
            ret = api.getwithdrawalhistory(currency, count)
        except Exception as err:
            logging.info(err)
            eprint('Error getting wd history: ' + str(err))
        else:
            ret = json.dumps(ret)
            return(ret)
        
    
    # program execution logic
        
    if ticker:
            if debug:
                    print('Ticker call.')
            ret = get_ticker(pair)
            print(ret)
                
    if deposit_address:
            if debug:
                    print('Deposit address call')
            ret = get_deposit_address(currency)
            print(ret)
    if balances:
            if debug:
                    print('Get all balances call')
            ret = get_balances()
            print(ret)

    if balance:
            if debug:
                    print('Get balance call')
            ret = get_balance(currency)
            print(ret)
                

    if buy_limit:
            if debug:
                    print('Buy limit call')
            ret = buy_limit_order(pair, amount, price)
            print(ret)
    if sell_limit:
            if debug:
                    print('Sell limit call')
            ret = sell_limit_order(pair, amount, price)
            print(ret)

    if cancel_order:
            if debug:
                    print('Cancel order call')
            ret = cancel(order_id)
            print(ret)
            
    if withdraw and withdrawal_enabled:
            if debug:
                    print('Withdrawal call')
            ret = do_withdraw(currency, amount, address)
            print(ret)
            
    if withdrawal_history:
            if debug:
                    print('Withdrawal history call')
            ret = wd_history(currency, count)
            print(ret)
            
            
# start up            
if __name__ == "__main__":
    main(sys.argv[1:])
