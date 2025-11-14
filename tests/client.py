#!/usr/bin/env python3
'''
Created on 20170119
Update on 20251114
@author: Eduardo Pagotto
'''

import logging
import time

from zencomm import setup_queue_logging

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '.'))

from sjsonrpc.syn import RPC_Client

URL = 'unix:///tmp/teste0.sock'

logger_listern = setup_queue_logging('./log/client.log')
logger = logging.getLogger('client')

def do_test(msg: str, client : RPC_Client):

    logger.info("client start.")

    for c in range(3):
        val = client.call().teste(f"{msg}---{c}......")
        logger.info(f"response {c}: {val}")
        time.sleep(1)

    logger.info("client stop.")

def teste1():
    try:
        with RPC_Client(URL) as client:
            do_test('SYNC TESTE1', client)

    except Exception as exp:
        logger.error(str(exp))

def teste2():

    try:
        client = RPC_Client(URL)
        client.connect()

        do_test('SYNC TESTE2',client)

        client.disconect()

    except Exception as exp:
        logger.error(str(exp))


def main():
    teste1()
    teste2()

if __name__ == '__main__':
    try:
        main()
    except Exception as exp:
        logger.exception('Falha %s', str(exp))

    logger.info('App desconectado')
