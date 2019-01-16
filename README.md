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


Using the command “help \<command name\>” will give complete information about the command and relevant parameters, formatted in a way you can copy and paste (replacing the addresses, transactions IDs, etc., as required). The format below shows the command with parameters followed by the response, in some cases parameters or responses are truncated with the term “\<snip\>”. Where noted, some commands only work with the regtest (Regression Test) network. Many commands will return “null” for qtum-qt and return nothing for command line systems.
