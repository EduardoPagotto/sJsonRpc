#!/usr/bin/env python3
'''
Created on 20251030
Update on 20251114
@author: Eduardo Pagotto
'''

import asyncio
import logging

from zencomm import setup_queue_logging

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '.'))

from sjsonrpc.asy import RPC_Client

URL = 'unix:///tmp/teste0.sock'

logger_listern = setup_queue_logging('./log/async_client.log')
logger = logging.getLogger('async_client')

async def do_test(msg: str, client : RPC_Client):

    logger.info("client start.")

    for c in range(3):
        val = await client.call().teste(f"{msg}---{c}......")
        logger.info(f"response {c}: {val}")
        await asyncio.sleep(1)

    logger.info("client stop.")

async def teste1():
    try:
        async with RPC_Client(URL) as client:
            await do_test('TESTE1', client)

    except Exception as exp:
        logger.error(str(exp))

async def teste2():

    try:
        client = RPC_Client(URL)
        await client.connect()

        await do_test('TESTE2',client)

        await client.disconect()

    except Exception as exp:
        logger.error(str(exp))

async def main():
    await teste1()
    await teste2()

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client shutting down gracefully...")
    except asyncio.CancelledError:
        print("Client task cancelled gracefully...")
