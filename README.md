# Qtum-Block-Ripper
A simple program to extract parameters from Qtum blocks.

A program to walk the Qtum blockchain and extract the Bits value, which sets the target for the SHA-256 hash on the next block.
The ripper uses qtum-cli to query a running qtumd server applicaion to grab the block number and Bits for each block. Run from the same directory as qtum-cli.

Sample printed output starting with block 37000 for 10 blocks:

Qtum Block Ripper 10/31/2017
block,time,mediantime,difficulty bits, difficulty
37000,1509491056,1509490016,502789,2186791.77659018
37001,1509491104,1509490464,455652,2413014.428906271
37002,1509491328,1509490608,384456,2859871.742306012
37003,1509491552,1509490816,456541,2408315.683717344
37004,1509491664,1509490976,542142,2028056.949212568
37005,1509492224,1509491056,525200,2093478.390251333
37006,1509492256,1509491104,968337,1135446.492863538
37007,1509492288,1509491328,786773,1397474.049770391
37008,1509492304,1509491552,639253,1719968.229417774
37009,1509492592,1509491664,499416,2201561.124513432


### getstakinginfo

Returns staking-related information.

* “enabled”: true means the wallet was launched with staking allowed (command line option `-staking=false` was not used)
* “staking”: true means the wallet is staking (decrypted, mature coins, blockchain synced)
* “errors” gives the various errors (rare)
* “currentblocktx” gives the number of transactions in a block mined by the wallet
* “pooledtx” gives the number of transactions waiting in the mempool
* “difficulty” gives the PoS target difficulty for the current block
* “search-interval” gives either the time in seconds since the wallet began staking or the time since the wallet’s most recent block reward, here one day and one minute
* “weight” gives the wallet weight in Satoshis, move the decimal point eight digits to the left to give these weights in units, here wallet weight is 148 QTUM and the network weight is 12.23 million
* “netstakeweight” gives the estimated network weight
* “expected time” gives an estimate of the average expected time to a block reward in seconds, here 4.59 months

```
getstakinginfo

{
  "enabled": true,
  "staking": true,
  "errors": "",
  "currentblocktx": 0,
  "pooledtx": 2,
  "difficulty": 4096615.946734428,
  "search-interval": 86460,
  "weight": 14807063425,
  "netstakeweight": 1223152433452116,
  "expectedtime": 11897280
}
```

