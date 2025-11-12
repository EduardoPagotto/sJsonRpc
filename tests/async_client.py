#!/usr/bin/env python3
'''
Created on 20251030
Update on 20251112
@author: Eduardo Pagotto
'''

import asyncio
import json
import logging
from typing import Any
from urllib.parse import urlparse

from zencomm import ProtocolCode, setup_queue_logging
from zencomm.asy.protocol import Protocol
from zencomm.asy.socket import socket_client

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '.'))

from sjsonrpc.asy import ProxyObject, ConnectionControl

URL = 'unix:///tmp/teste0.sock'

logger_listern = setup_queue_logging('./log/async_client.log')
logger = logging.getLogger('async_client')


class ConnectionRemote(ConnectionControl):
    def __init__(self, url):
        super().__init__(url)

    async def exec(self, input_rpc : dict, *args, **kargs) -> dict:

        timeout = 60
        parsed_url = urlparse(self.getUrl())

        result : dict = {}

        try:
            reader, writer = await socket_client(parsed_url, timeout)
            if reader and writer:

                    p = Protocol(reader, writer)

                    payload = json.dumps(input_rpc)

                    await p.sendString(ProtocolCode.COMMAND, payload)
                    c, m = await p.receiveString()
                    if c == ProtocolCode.RESULT:
                        result = json.loads(m)
                    else:
                        raise Exception(m)

                    await p.sendClose('bye')

        except asyncio.TimeoutError:
            logger.error(f"Connection to {parsed_url.geturl()} timed out after {timeout} seconds.")

        except FileNotFoundError:
            logger.error(f"Unix socket not found at {parsed_url.geturl()}")

        except ConnectionRefusedError:
            logger.error(f"Connection to {parsed_url.geturl()} refused.")

        except asyncio.IncompleteReadError:
            logger.error(f"Client {parsed_url.geturl()} disconnected unexpectedly.")

        except ConnectionResetError:
            logger.error(f"Client {parsed_url.geturl()} forcibly closed the connection.")

        # except asyncio.CancelledError:
        #     logger.error("Client task cancelled gracefully..")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")

        finally:
            logger.info("client stop.")


        return result

class ClientRCP(object):
    def __init__(self, addr) -> None:
        self.comm = ConnectionRemote(addr)

    def __rpc(self) -> Any:
        return ProxyObject(self.comm)

    async def teste(self, nome : str) -> str:
        return await self.__rpc().teste(nome) # pyright: ignore[reportAttributeAccessIssue]


async def main():

    logger.info("client start.")

    client = ClientRCP(URL)
    val = await client.teste("estuardo")
    logger.info(f"Recebido {val}")

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client shutting down gracefully...")
    except asyncio.CancelledError:
        print("Client task cancelled gracefully...")
