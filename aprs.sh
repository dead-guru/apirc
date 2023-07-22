#!/bin/bash
rtl_fm -f 144.80M - | direwolf -c ./dire_sdr.conf -r 24000 -D 1 -
