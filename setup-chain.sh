#!/bin/sh
ADDR=$(../bitcoin/src/bitcoin-cli -regtest getnewaddress)
echo $(../bitcoin/src/bitcoin-cli -regtest generatetoaddress 200 $ADDR)

