#!/bin/sh
../bitcoin/src/bitcoind -regtest -txindex -rpcworkqueue=1000 -fallbackfee=0.0002 -par=2

