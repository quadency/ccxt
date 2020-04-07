# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.bittrex import bittrex


class bittrexglobal(bittrex):

    def describe(self):
        return self.deep_extend(super(bittrexglobal, self).describe(), {
            'id': 'bittrexglobal',
            'name': 'Bittrex Global',
            'certified': False,
            'hostname': 'global.bittrex.com',
        })
