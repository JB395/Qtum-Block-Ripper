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


### getwalletinfo

Returns information about the wallet:

* “walletname" – the name of the wallet.dat file currently loaded
* "walletversion" – not the software client version, use `getnetworkinfo` to check this
* "balance" – balance in QTUM
* "stake" – any balance currently committed to a stake
* "unconfirmed_balance" – any balance that hasn’t been published in the next blocks
* "immature_balance" – any coinbase (Proof of Work) balance that does not have 500 confirmations, seen only for regtest.
* "txcount" – the total number of transactions in the wallet
* "keypoololdest" – the Unix epoch timestamp in seconds for the oldest key in the key pool
* "keypoolsize" - how many new keys are pre-generated
* "keypoolsize_hd_internal" - how many new keys are pre-generated for internal use (used for change addresses)
* "unlocked_until" – the Unix epoch time in seconds that the wallet is unlocked, or 0 if the wallet is locked, this field is omitted for unencrypted wallets.
* "paytxfee" – the transaction fee in QTUM per 1,000 bytes
* "hdmasterkeyid" – a Hash 160 of the hierarchical deterministic (HD) master public key, this field is omitted if HD is not enabled

```
getwalletinfo
{
  "walletname": "wallet.dat",
  "walletversion": 130000,
  "balance": 1.53160855,
  "stake": 0.00000000,
  "unconfirmed_balance": 0.00000000,
  "immature_balance": 0.00000000,
  "txcount": 94,
  "keypoololdest": 1507072726,
  "keypoolsize": 952,
  "unlocked_until": 0,
  "paytxfee": 0.00000000,
  "hdmasterkeyid": "c1c081490c4dc42b3e3431683052df36bc583fbe5"
}
```

