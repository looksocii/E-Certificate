from getFileName import file_name
from issueCredentialTool import *
import json

def issue():
    with open('issue_conf.json') as file_obj:
        conf = json.load(file_obj)
    send_address = conf['send_address']

    rootList = list()
    # get manifest file
    file_dir = 'data'
    croot, cdirs, cfiles = file_name(file_dir)
    for dirs in cdirs:
        with open(file_dir + '\\' + dirs + '\\manifest.json') as file_obj:
            data = json.load(file_obj)
        root = data['manifest']['value']
        rootList.append(root)
    rootSet = set(rootList)
    if len(rootSet) == 1:
        raw_txn = create_raw_txn(send_address, list(rootSet)[0])  # list(rootSet)[0] = root
        result = sign_send_txn(raw_txn[0:-1])

        if 'error' in result:
            print('Error: ' + result['error'])
        else:
            print('TxID: ' + result['txid'])

            chain = bitcoin_cmd('getblockchaininfo')['chain']

            # add txid to manifest.json
            file_dir = 'data'
            croot, cdirs, cfiles = file_name(file_dir)
            for dirs in cdirs:
                # get signature
                with open(file_dir + '\\' + dirs + '\\manifest.json') as file_obj:
                    data = json.load(file_obj)
                data['signature']['txId'] = result['txid'].strip()
                data['signature']['chain'] = chain

                # write back to manifest.json
                filename = file_dir + '\\' + dirs + '\\manifest.json'
                with open(filename, 'w') as file_obj:
                    json.dump(data, file_obj, indent=2)

            print('chain: ', chain)

if __name__ == '__main__':
    issue()
