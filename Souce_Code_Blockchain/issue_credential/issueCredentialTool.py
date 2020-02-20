# OP_RETURN.py
#
# Python script to generate and retrieve OP_RETURN bitcoin transactions
#
# Copyright (c) Coin Sciences Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import subprocess, json, binascii, struct, re, hashlib, os

# Python 2-3 compatibility logic

try:
    basestring
except NameError:
    basestring = str

# User-defined quasi-constants

BITCOIN_IP = '127.0.0.1'  # IP address of your bitcoin node

BITCOIN_PATH = 'C:\\Program Files\\Bitcoin\\daemon\\bitcoin-cli'  # path to bitcoin-cli executable on this server

BTC_FEE = 0.0001  # BTC fee to pay per transaction
BTC_DUST = 0.00001  # omit BTC outputs smaller than this

MAX_BYTES = 80  # maximum bytes in an OP_RETURN (80 as of Bitcoin 0.11)
MAX_BLOCKS = 10  # maximum number of blocks to try when retrieving data

NET_TIMEOUT = 10  # how long to time out (in seconds) when communicating with bitcoin node

#bitcoin-cmd
def bitcoin_cmd(command, *args):  # more params are read from here

    sub_args = [BITCOIN_PATH]

    sub_args.append(command)

    for arg in args:
        sub_args.append(json.dumps(arg) if isinstance(arg, (dict, list, tuple)) else str(arg))

    raw_result = subprocess.check_output(sub_args).decode("utf-8").rstrip("\n")

    try:  # decode JSON if possible
        result = json.loads(raw_result)
    except ValueError:
        result = raw_result

    return result

#get unspent-output
def select_inputs(total_amount):
    # List and sort unspent inputs by priority

    unspent_inputs = bitcoin_cmd('listunspent')
    if not isinstance(unspent_inputs, list):
        return {'error': 'Could not retrieve list of unspent inputs'}

    unspent_inputs.sort(key=lambda unspent_input: unspent_input['amount'] * unspent_input['confirmations'],
                        reverse=True)

    # Identify which inputs should be spent

    inputs_spend = []
    input_amount = 0

    for unspent_input in unspent_inputs:
        inputs_spend.append(unspent_input)

        input_amount += unspent_input['amount']
        if input_amount >= total_amount:
            break  # stop when we have enough

    if input_amount < total_amount:
        return {'error': 'Not enough funds are available to cover the amount and fee'}

    # Return the successful result

    return {
        'inputs': inputs_spend,
        'total': input_amount
    }

#create raw txn
def create_raw_txn(send_address, metadata):
    balance = bitcoin_cmd('getbalance')
    send_amount = format(balance - BTC_FEE, '.8f')
    output_amount = balance

    inputs_spend = select_inputs(output_amount)
    if 'error' in inputs_spend:
        return {'error': inputs_spend['error']}

    inputs = list()
    for input in inputs_spend['inputs']:
        dic = dict()
        dic['txid'] = input['txid']
        dic['vout'] = input['vout']
        inputs.append(dic)

    #change_amount = inputs_spend['total'] - output_amount
    #print("change_amount: ", change_amount)

    #print("inputs: ", inputs)

    #change_address = bitcoin_cmd('getrawchangeaddress')
    #print("change_address: ", change_address)

    outputs = {send_address: send_amount}
    outputs['data'] = metadata

    #if change_amount >= OP_RETURN_BTC_DUST:
        #outputs[send_address] = change_amount

    #print("outputs: ", outputs)

   # raw_txn = create_txn(inputs_spend['inputs'], outputs, metadata, len(outputs))
    #print("raw_txn: ", str(inputs) + "\t" + str(outputs))
    #raw_txn = bitcoin_cmd('createrawtransaction', inputs, outputs)
    raw_txn = bitcoin_cmd('createrawtransaction', inputs, outputs)

    return raw_txn

def sign_send_txn(raw_txn):
    signed_txn = bitcoin_cmd('signrawtransactionwithwallet', raw_txn)
    #print('signed_txn: ', signed_txn)
    if not ('complete' in signed_txn and signed_txn['complete']):
        return {'error': 'Could not sign the transaction'}

    send_txn = bitcoin_cmd('sendrawtransaction', signed_txn['hex'])
    #print('isinstance: ', isinstance(send_txn, basestring))
    #print('send_txn: ', send_txn)
    #print('len: ', len(send_txn))
    if not (isinstance(send_txn, basestring)):
        return {'error': 'Could not send the transaction'}

    return {'txid': send_txn}

def test():
    #create raw txn
    send_address = '2N8L8TzTRvzjok9nhi5mkeFvGpcYiVHifpE'
    metadata = 'ec1eebc135c3c2259321471a4ea762a3b9914177e6718417b094a7a613d78dbb'

    raw_txn = create_raw_txn(send_address, metadata)
    print("raw_txn: ", raw_txn)

    decode_rawtxn = bitcoin_cmd('decoderawtransaction', raw_txn[0:-1])
    print("decode_rawTxn: ", decode_rawtxn)

    txid = sign_send_txn(raw_txn[0:-1])
    print("txid: ", txid)

    bc_info = bitcoin_cmd('getblockchaininfo')
    chain = bc_info['chain']
    print('chain: ', chain)

if __name__ == '__main__':
    test()
