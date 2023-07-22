#!/usr/bin/env python3
import asyncio
import logging
import os
import irc.client
import irc.client_aio

from ax253 import Frame
import kiss

from functools import partial

MYCALL = os.environ.get("MYCALL", "N0CALL")
KISS_HOST = os.environ.get("KISS_HOST", "10.10.10.91")
KISS_PORT = os.environ.get("KISS_PORT", "8001")

server = os.environ.get('IRC_HOST', "irc.dead.guru")
port = int(os.environ.get('IRC_PORT', 6697))
channel = os.environ.get('CHANNEL_NAME', "#spau")
nickname = os.environ.get('BOT_NICK', "aprsbot")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

async def main():
    loop = asyncio.get_event_loop()
    
    c = await irc.client_aio.AioReactor(loop=loop).server().connect(
            server, port, nickname, connect_factory=irc.connection.AioFactory(ssl=True)
        )
    
    transport, kiss_protocol = await kiss.create_tcp_connection(
        host=KISS_HOST,
        port=KISS_PORT,
        loop=loop,
    )
    
    c.privmsg(channel, '[APRS] Starting...')
    
    async for frame in kiss_protocol.read():
        print('Got frame')    
        c.privmsg(channel, str(frame))
        

if __name__ == "__main__":
    asyncio.run(main())
