#!/usr/bin/env python3
import asyncio
import logging
import os
import irc.client
import irc.client_aio

from ax253 import Frame
from datetime import datetime
import kiss
import aprslib

MYCALL = os.environ.get("MYCALL", "N0CALL")
KISS_HOST = os.environ.get("KISS_HOST", "10.10.10.91")
KISS_PORT = os.environ.get("KISS_PORT", "8001")

server = os.environ.get('IRC_HOST', "irc.dead.guru")
port = int(os.environ.get('IRC_PORT', 6697))
channel = os.environ.get('CHANNEL_NAME', "#spau")
nickname = os.environ.get('BOT_NICK', "aprsbot")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG) ## TODO: Make logging level configurable

def parse_frame(date, frame):
    try:
        parsed = aprslib.parse(str(frame))
    except (aprslib.ParseError, aprslib.UnknownFormat) as exp:
        logger.error(f"Failed to parse frame: {frame}")
        return str(frame)
    formatted_string = date.strftime('%H:%M:%S.%f')[:-3] + " " + "{} -> {} -> {}:".format(parsed["from"], parsed["via"], parsed["to"])
    formatted_string += " <{:.4f} {:.4f}>".format(parsed["latitude"], parsed["longitude"]) if "longitude" in parsed and "latitude" in parsed else ""
    formatted_string += " tUNIT: " + ",".join(parsed["tUNIT"]) if "tUNIT" in parsed else ""
    formatted_string += " tPARM: " + ",".join(parsed["tPARM"]) if "tPARM" in parsed else ""
    formatted_string += " tEQNS: " + ",".join([''.join(str(i)) for i in parsed["tEQNS"]]) if "tEQNS" in parsed else ""
    formatted_string += " tBITS: {}".format(parsed["tBITS"]) if "tBITS" in parsed else ""
    formatted_string += " {}".format(parsed["comment"]) if "comment" in parsed else ""
    formatted_string += " {}".format(parsed["title"]) if "title" in parsed else ""
    return formatted_string

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
    
    irc_client.privmsg(channel, 'Starting...')
    
    async for frame in kiss_protocol.read():
        time = datetime.utcnow()
        
        logger.debug(f"Received frame: {frame}")   
        irc_client.privmsg(channel, parse_frame(time, frame))
        

if __name__ == "__main__":
    asyncio.run(main())
