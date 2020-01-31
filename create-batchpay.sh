#!/bin/bash

SPEND_TO=$(
printf "{ ";
for x in {1..10}; do printf "\"$(../bitcoin/src/bitcoin-cli -regtest getnewaddress)\"";
                     printf ": \""0.$RANDOM"\", " ; done
printf "\"$(../bitcoin/src/bitcoin-cli -regtest getnewaddress)\"";
printf ": \""0.$RANDOM"\"";
printf " }";
)

echo "$SPEND_TO"


../bitcoin/src/bitcoin-cli -regtest sendmanycompacted "$SPEND_TO" 4 0
