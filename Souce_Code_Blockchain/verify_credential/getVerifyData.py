import json, subprocess, sys

BITCOIN_PATH = 'C:\\Program Files\\Bitcoin\\daemon\\bitcoin-cli'  # path to bitcoin-cli executable on this server

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

def get_issuerAddress(txid):
    tx = bitcoin_cmd('gettransaction', str(txid))
    address = tx['details'][0]['address']
    #print('address: ', address)
    return address

def get_merkleRoot(txid):
    tx = bitcoin_cmd('gettransaction', str(txid))
    tx_hex = bitcoin_cmd('decoderawtransaction', tx['hex'])
    asm = tx_hex['vout'][-1]['scriptPubKey']['asm'].split()
    data = asm[-1]
    #print('data: ', data)
    return data



