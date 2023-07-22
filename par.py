#!/usr/bin/env python3
import aprslib
from datetime import datetime

packets = open('packets.log', 'r')

for packetString in packets:
    
    formatted_string = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3] + " " + "{} -> {} -> {}:".format(parsed["from"], parsed["via"], parsed["to"])
    formatted_string += " <{:.4f} {:.4f}>".format(parsed["latitude"], parsed["longitude"]) if "longitude" in parsed and "latitude" in parsed else ""
    formatted_string += " tUNIT: " + ",".join(parsed["tUNIT"]) if "tUNIT" in parsed else ""
    formatted_string += " tPARM: " + ",".join(parsed["tPARM"]) if "tPARM" in parsed else ""
    formatted_string += " tEQNS: " + ",".join([''.join(str(i)) for i in parsed["tEQNS"]]) if "tEQNS" in parsed else ""
    formatted_string += " tBITS: {}".format(parsed["tBITS"]) if "tBITS" in parsed else ""
    formatted_string += " {}".format(parsed["comment"]) if "comment" in parsed else ""
    formatted_string += " {}".format(parsed["title"]) if "title" in parsed else ""
    #print(parsed)
    print(formatted_string)