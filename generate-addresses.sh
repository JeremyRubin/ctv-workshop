#!/bin/bash
for x in {1..100}; do echo $(../bitcoin/src/bitcoin-cli -regtest getnewaddress) 0.$RANDOM ; done



