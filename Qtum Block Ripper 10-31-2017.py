version = "10/31/2017"
'''
Qtum Block Ripper.py (QBR)

Copyright (c) 2017 Jackson Belove
Beta software, use at your own risk
MIT License, free, open software for the Qtum Community

A program to walk the Qtum blockchain and extract the Bits value, which sets
the target for the SHA-256 hash on the next block.
Uses qtum-cli to send RPC queries to the qtumd server application
to send getblockhash and getblock queries to the blockchain to grab the
block number and Bits for each block. Run from the same directory as qtum-cli.

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

09/31/2017 Repurposed from QtumMon 10-27-2017

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

logLabels = 'block,time,mediantime,difficulty bits, difficulty'

import subprocess
import time
from time import localtime, strftime, sleep
from datetime import datetime
import smtplib                          # email sending function
from email.mime.text import MIMEText    # for email formatting
import os, sys                          # for file operations
from timeit import default_timer as timer
from array import *                     # for arrays

block = 37000         # starting block number, working forwards
numBlocks = 10        # number of blocks to collect


def parse_number(field, offset, lenData, periodAllowed):
    '''
    parse the global variable "data" which is the response from qtum-cli calls.
    Search for the text "field", then get the digit characters starting 
    "offset" characters from the start of the field, and search through at
    least "lenData" characters, and respond to a period "." if "periodAllowed"
    is True.
    
    For example, to find the balance from the qtum-cli command getinfo:
                       periodAllowed = True
                       v
    ..."balance": 14698.3456000, \r\n...
                  ^    
                  offset = 10 characters from start of balance
    '''
    global data
    
    temp = ' '
	
    dataIndex = data.find(field, 0, lenData)

    i = dataIndex + offset  	# point at the first digit
	
    if dataIndex > 0:  # found field
        while i <= lenData - 1:
            
            if data[i] >= '0' and data[i] <= '9':
                temp += data[i]
            elif data[i] == "." and periodAllowed == True:  # if period allowed
                temp += data[i]
            elif data[i] == ",":
                break
            elif (i == dataIndex + offset) and (data[i] == "-"):  # allow negative sign
                temp += data[i]                                   # first character only
            else:  # how to find \r at end of response, like for estimated time?
                # print("QM error, bad character in ", field)
                break
                    
            i += 1	
            if i >= lenData:
                break
            
        return(temp)
            
    else:
        return(-1)      # an error

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# parse alphanumeric text like "True", "xyz@gmail.com" and "HP8200"

def parse_alphanum(field, offset, lenData):
    # parse against the global variable "data"
    
    global data
    
    temp = ''   # AAA
    
    dataIndex = data.find(field, 0, lenData)
    
    i = dataIndex + offset  	# point at the first digit
	
    if dataIndex > 0:  # found field
        # allow characters 0..9, @..Z, a..z  AAA
        while i <= lenData - 1:

            # print("data[i] = ", data[i])
            
            if (data[i] >= 'a' and data[i] <= 'z') or +\
               (data[i] >= '@' and data[i] <= 'Z') or +\
               (data[i] >= '0' and data[i] <= '9') or +\
               (data[i] == '.') or +\
               (data[i] == '-'):
                temp += data[i]
            elif data[i] == "," or data[i] == "'\'":     # for getinfo proof-of-stake AAA
                break
            else:
                # print("QM error, bad character in ", field) #PY3
                # print "QM error, bad character in " + field #PY2
                break
                    
            i += 1
                    
            if i >= lenData:
                break
        return(temp)
            
    else:
        return(-1)   # an error
        
def parse_logical(field, offset, lenData):
    # parse against the global variable "data"

    global data
    
    temp = ''
    
    dataIndex = data.find(field, 0, lenData)
    
    i = dataIndex + offset  	# point at the first digit

    if dataIndex > 0:  # found field
        while i <= lenData - 1:
            if data[i] >= 'a' and data[i] <= 'z':
                temp += data[i]
            elif data[i] == ",":
                break
            else:
                print("QM error, bad character in ", field)   #PY3
                # print "QM error, bad character in " + field #PY2
                break
                    
            i += 1
                    
            if i >= lenData:
                break    

        # print("field =", field, "temp =", temp)
        
        if temp == "true":
            return(True)
        elif temp == "false":	
            return(False)
 
    else:
        return(-1)   # an error
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                            
print("Qtum Block Ripper", version)
print(logLabels)

endBlock = block + numBlocks

while block < endBlock:

    strBlock = str(block)    
    params = "qtum-cli getblockhash " + strBlock

    try:
        blockHashRaw = str(subprocess.check_output(params, shell = True))
    except:
        print("ERROR, no response from qtumd")  

    # print(blockHashRaw) # b'c959cef0fa25a6df938b3b9b1045f95488e393de6462c9befb17305795bd1d58\r\n'

    blockHash = blockHashRaw[2:66]
    # print(blockHash)

    params = "qtum-cli getblock " + blockHash

    try:
        output = str(subprocess.check_output(params, shell = True))
    except:
        print("ERROR, no response from qtumd")

    data = str(output)
    lenData = len(data)
    
    # print(data)
    
    '''
    b'{\r\n  "hash": "c959cef0fa25a6df938b3b9b1045f95488e393de6462c9befb17305795bd1d58",\r\n  
    "confirmations": 46,\r\n  "strippedsize": 1557,\r\n  "size": 1593,\r\n  "weight": 6264,\r\n
    "height": 37000,\r\n  "version": 536870912,\r\n  "versionHex": "20000000",\r\n
    "merkleroot": "1376456b1de73600cf422909e397a6d0cae6d7a1e18769538c4c56ef6de36c04",\r\n  
    "hashStateRoot": "8acb5b036b28eabb62321c6d907e0e09a05be1eda4fb3fc69e6817f84a25303b",\r\n  
    "hashUTXORoot": "37a4fe968c0dfe6e48f54201e64bf8e42fe7081f8bb299a999297919c8eca8ef",\r\n  
    "tx": [\r\n    "950673a0f02309b9f788a42aa88cdc4d741f863b02fc0f5c6ec12fe7f7a0e462", \r\n    
    "cb918eaadae2f7a3cd58f06ad6e2a05edae35b0a8ffedab4f563e8942d4ed287", \r\n    
    "068e2eaf50a408e66c18588503cd825dbf7e34ae606138e0cb7fc42a490f4408"\r\n  ],\r\n  
    "time": 1509491056,\r\n  "mediantime": 1509490016,\r\n  "nonce": 0,\r\n  
    "bits": "1a07ac05",\r\n  "difficulty": 2186791.77659018,\r\n  "chainwork": 
    "0000000000000000000000000000000000000000000000091bec61e42b94c115",\r\n  
    "previousblockhash": "e3d3b2fa08362d8eedc75f58ad3d6bfac520cc464c46bb812b86225ab2efc2ac",\r\n  
    "nextblockhash": "5bbed9dc60b1cc3bc7a74b63eb9fbfc6f357555608a3e45d902936b7da2c966d",\r\n  
    "flags": "proof-of-stake",\r\n  "proofhash": "0025af91ac741d6445d48cc751c36b9b3adbd6791387c0afa241ca8559fae924",\r\n  
    "modifier": "740dabc5cc8a6e87fa83b55e51a25cf14267c6027579decca9aa5cc0a7abe0b1",\r\n  
    "signature": "304402205493eb0869efeef1c1a95d4edea63a2399f3d4bc6b32aadf903bb98a1ccc1c0502
    200e74c7153492ce730b8ad979bd876e20c3bacb12b6e6cd2a6f5de59be5b3d8c0"\r\n}\r\n'
    '''
     
    # print("lenData =", lenData)     # lenData = 568
    
    time = int(parse_number("time", 7, lenData, False))
    # print("time = ", time)

    mediantime = int(parse_number("mediantime", 13, lenData, False))  
    # print("mediantime = ", mediantime)
    
    bits = parse_alphanum("bits", 8, lenData) 
    # print("difficulty bits = ", bits)
    bitsA = bits[2:]
    # print(bitsA)
    bitsInt = int(bitsA, 16)

    # print(bitsInt)              
    
    # https://en.bitcoin.it/wiki/Difficulty

    '''
    hexBits = int(bits, 16)
    exp = hexBits >> 24
    mant = hexBits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    target_str = target_hexstr.decode('hex')
    print(target_str)
    '''
     
    difficulty = float(parse_number("difficulty", 13, lenData, True))
    # print("difficulty = ", difficulty)

    temp =  str(block) + "," + str(time) + "," + str(mediantime) + "," + str(bitsInt) + "," + str(difficulty)
    print(temp)

    block += 1
    
sys.exit()

