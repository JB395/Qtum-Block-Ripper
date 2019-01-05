version = "12/28/2018"
'''
Qtum Block Ripper.py (QBR)
Copyright (c) 2018 Jackson Belove
Beta software, use at your own risk
MIT License, free, open software for the Qtum Community

A program to walk the Qtum blockchain and print the block size
and weight. Uses qtum-cli to send RPC queries to the qtumd server application
to send getblockhash and getblock queries to the blockchain to grab the
block number and information for each block. Run from the same directory as qtum-cli.

Sample printed output starting with block 200,000 for 10 blocks:

Qtum Block Ripper 12/28/2018
block, time, size, weight, minutes
200000,1532993104,2124,8388,0
200001,1532993216,1629,6408,0
200002,1532993376,10452,41700,0
200003,1532993424,1404,5508,0
200004,1532993472,960,3732,0
200005,1532993568,1479,5808,0
200006,1532993712,5757,22920,0
200007,1532993744,926,3596,0
200008,1532993920,2224,8788,0
200009,1532993952,927,3600,0

"minutes" gives approximate minutes until finishing, depending on the speed of
your computer, and the formula can be adjusted in the print statement at the bottom.

12/28/2018 Repurposed from Qtum Block Ripper 10-27-2017
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

# logLabels = 'block, time, mediantime, strippedsize, size, weight, difficulty bits, difficulty'
logLabels = 'block, time, size, weight, minutes'

import subprocess
import time
from time import localtime, strftime, sleep
from datetime import datetime
import smtplib                          # email sending function
from email.mime.text import MIMEText    # for email formatting
import os, sys                          # for file operations
from timeit import default_timer as timer
from array import *                     # for arrays

block = 200000                # starting block number, working forwards
numBlocks = 10                # number of blocks to collect


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

# skip over "strippedsize" to return "size"

def parse_size(field, offset, lenData, periodAllowed):
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

    start = dataIndex + 13      # skip past "strippedsize"

    # print("start =", start)

    dataIndex = data.find(field, start, lenData)    

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
# parse alphanumeric text

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
    b'{\r\n  "hash": "06a0ffd34d9b89e20dcf6039b84372372bd875f01c1ac4b509892d58fa15e96f",\r\n
    "confirmations": 95055,\r\n  "strippedsize": 2088,\r\n  "size": 2124,\r\n
    "weight": 8388,\r\n  "height": 200000,\r\n  "version": 536870912,\r\n
    "versionHex": "20000000",\r\n  "merkleroot": "5e68b72509a52a655be087bfd38d3a4328ed626b9e13ccceb994272c4839a2dc",\r\n
    "hashStateRoot": "d4467228309388969e5651d9c8085d5b09b419dd79524bc988842cac60483b40",\r\n
    "hashUTXORoot": "e8df6bd527f6d3144be7b02ba724aca9c3e18f42014891ee3f87eba9462ef979",\r\n
    "tx": [\r\n    "960c776f119d0a1f28199d37b6f3daf2d61986aa36bc59d9973e0019b1fc27de",\r\n
    "e61a5b557bc33e1ef810c655dd7fc9146404a369c3f7f8a61db0b09995b90674",\r\n
    "10f6a2d9a14c2298e69e84606c8db064724e6d93dc75ef7a4c55c0d64a8489f9",\r\n
    "6f272945a2c4fad5729e7cb20bbf0a4a1165a686a2f70a7e99fd2f1497274163"\r\n  ],\r\n
    "time": 1532993104,\r\n  "mediantime": 1532992416,\r\n  "nonce": 0,\r\n  "bits":
    "1a068067",\r\n  "difficulty": 2580446.83494216,\r\n
    "chainwork": "00000000000000000000000000000000000000000000008f4baca9000caf9cfb",\r\n
    "previousblockhash": "384149db1c5269fdc72cf1629ec5f3868fec4d2fb01dee2011f5a39c0f028b5b",\r\n
    "nextblockhash": "6d4ae81a2a609b7ee6c9bbce01facf52b1ba4a851d2afc77f7261ea3284bd7ea",\r\n
    "flags": "proof-of-stake",\r\n  "proofhash": "0000000000000000000000000000000000000000000000000000000000000000",\r\n
    "modifier": "fce1c5f64c429e99f3cd942e79994eedf1909b713f4c626059c6806962459a16",\r\n
    "signature": "30450221008d180783930a922cffdfe8fb97ca1b623d7f20063c427bfc2cda5e532d470621022002d0ab4e1c3cdbc2d81c4759eb68874431b22d881a2f161ab3ea52a28e4099c5"\r\n
    }\r\n'
    '''
     
    # print("lenData =", lenData)     # lenData = 568

    size = int(parse_size("size", 7, lenData, False))

    weight = int(parse_number("weight", 9, lenData, False))
    
    time = int(parse_number("time", 7, lenData, False))

    # print("time = ", time)

    # mediantime = int(parse_number("mediantime", 13, lenData, False))  
    # print("mediantime = ", mediantime)
 
    # bits = parse_alphanum("bits", 8, lenData) 
    # print("difficulty bits = ", bits)
    # bitsA = bits[2:]
    # print(bitsA)
    # bitsInt = int(bitsA, 16)

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
     
    # difficulty = float(parse_number("difficulty", 13, lenData, True))
    # print("difficulty = ", difficulty)

    # minutes = blocks left * (60 seconds / seconds per block for this computer)

    # temp =  str(block) + "," + str(time) + "," + str(mediantime) + "," + str(size) + "," + str(weight) + "," + str(bitsInt) + "," + str(difficulty)
    temp =  str(block) + "," + str(time) + "," + str(size) + "," + str(weight) + "," + str(int((endBlock - block) * 0.061))

    print(temp)

    block += 1
    
sys.exit()
