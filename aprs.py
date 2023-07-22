#!/usr/bin/env python3
import asyncio
import logging
import os
import irc.client
import irc.client_aio

from ax253 import Frame
import kiss

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
    logger.info(f"Connecting to {server}:{port} as {nickname}")
    loop = asyncio.get_event_loop()
    
    irc_client = await irc.client_aio.AioReactor(loop=loop).server().connect(
            server, port, nickname, connect_factory=irc.connection.AioFactory(ssl=True) ## TODO: Make SSL optional and add password support
        )
    logger.info(f"Connected to {server}:{port} as {nickname}")
    
    transport, kiss_protocol = await kiss.create_tcp_connection(
        host=KISS_HOST,
        port=KISS_PORT,
        loop=loop,
    )
    
    irc_client.privmsg(channel, '[APRS] Starting...')
    
    async for frame in kiss_protocol.read():
        logger.debug(f"Received frame: {frame}")   
        irc_client.privmsg(channel, str(frame)) ## TODO: Parse frame and send to channel
        

if __name__ == "__main__":
    asyncio.run(main())
