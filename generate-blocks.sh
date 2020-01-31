#!/bin/sh
ADDR=$(../bitcoin/src/bitcoin-cli -regtest getnewaddress)
while true; do sleep 1; echo $(../bitcoin/src/bitcoin-cli -regtest generatetoaddress 1 $ADDR)  ; done

