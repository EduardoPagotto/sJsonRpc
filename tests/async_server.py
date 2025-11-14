#!/usr/bin/env python3
'''
Created on 20241001
Update on 20251114
@author: Eduardo Pagotto
'''

import asyncio
import json
import logging
import os
import signal
import sys
import threading

from zencomm.asy.protocol import Protocol
from zencomm import ProtocolCode, setup_queue_logging
from zencomm.asy.socket import SocketServer
from zencomm.utils import ExceptZen

sys.path.append(os.path.join(os.getcwd(), '.'))

from sjsonrpc.asy import RPC_Responser

URL = 'unix:///tmp/teste0.sock'

logger_listern = setup_queue_logging('./log/async_server.log')
logger = logging.getLogger('async_server')

class Responser(RPC_Responser):
    def __init__(self, target: object):
        super().__init__(target)

    async def __call__(self, *args, **kargs):
        """[execute exchange of json's messages with server RPC]
        """
        t_name = threading.current_thread().name
        logger.info(f'start {t_name}')

        stop_event : asyncio.Event = args[0]

        protocol = None
        try:
            protocol = Protocol(args[1], args[2], 30)

        except Exception as exp:
            logger.critical('fail creating connection: %s', str(exp))
            return

        count_to = 0

        while not stop_event.is_set():
            try:
                count_to = 0
                idRec, buffer = await protocol._receiveProtocol()
                if idRec == ProtocolCode.COMMAND:
                    await protocol.sendString(ProtocolCode.RESULT, json.dumps(await self.encode_exec_decode(json.loads(buffer.decode('UTF-8')))))

                elif idRec == ProtocolCode.CLOSE:
                    logger.debug(f'responser receive {buffer.decode('UTF-8')}')
                    break

            except asyncio.TimeoutError:
                count_to += 1
                logger.warning(f"timeout receiving: {count_to}")

            except asyncio.IncompleteReadError as ein:
                logger.error(f"incomplete read: {str(ein)}")
                break

            except ExceptZen as exx:
                logger.error(f"fail protocol {str(exx)}")
                break

            except Exception as exp:
                logger.error('%s exception error: %s', t_name, str(exp))
                break

        await protocol.close()

        logger.info(f'{t_name} finnished')


class ServerRPC(object):
    def __init__(self, url: str):
        self.server = SocketServer(url, Responser(self))
        self.nome = ''

    async def execute(self, stop_event:asyncio.Event):
        await self.server.execute(stop_event)

    async def set_nome(self, nome: str):
        self.nome = nome

    async def get_nome(self):
        return self.nome

    async def teste(self, nome):
        logger.info(f"Methodo TESTE recebido com {nome}")
        return "MSG_RECEBIDA_OK!!!!"


async def main():
    logger.info("server start.")

    # Set up a signal handler for graceful shutdown
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        #self.log.warning("Shutdown signal received...")
        stop_event.set()

    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)

    server = ServerRPC(URL)
    await server.execute(stop_event)

    logger.info("server stop.")

if __name__ == "__main__":
    asyncio.run(main())
