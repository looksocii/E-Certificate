import json
from checkingMerkleProof import checkingMerkleProof
from comparingHash import comparingHash
from checkingCausalRelationship import checking_causal_relationship
from getVerifyData import *
import time


def h2b(data):
    if data:
        return bytearray.fromhex(data)

def get_timestamp(datetime):
    timeArray = time.strptime(datetime, '%Y-%m-%dT%H:%M:%S:%fZ')
    timestamp = time.mktime(timeArray)
    return timestamp

def issuer_verify(txid, credential):
    # verify issuer authenticity
    # compare issuer's address in issuer.json with blockchain sender's address
    bol = False
    sender = get_issuerAddress(txid)
    with open('issuer.json') as file_obj:
        issuer_data = json.load(file_obj)
    addressList = issuer_data['addressList']
    for addressInfo in addressList:
        issuer_addr = addressInfo['address']
        if issuer_addr == sender:
            # check date True if (issue date > created)
            create_timestamp = get_timestamp(addressInfo['created'])
            issue_timestamp = get_timestamp(credential['createdAt'])
            if create_timestamp < issue_timestamp:
                print('\nissuer authenticity : True')
                bol = True
                return bol
            else:
                print('\nissuer authenticity : False')
                return bol

def verify():
    with open('data\\credential.json') as file_obj:
        credential = json.load(file_obj)

    with open('data\\manifest.json') as file_obj:
        data = json.load(file_obj)
    manifest = data['manifest']
    signature = data['signature']
    txid = signature['txId']

    issuer = issuer_verify(txid, credential)
    if issuer:
        #get MerkleRoot from blockchain
        MerkleRoot = get_merkleRoot(txid)

        # get selected credential's id and name
        checkingRoot = checkingMerkleProof(manifest)
        verifyList = checkingRoot.getVerifyList(manifest)
        print("verify list :", verifyList)
        print('\n')

        #comparing hash and checking merkle proof
        for id, name in verifyList.items():
            print(name)
            result = comparingHash(id, name, verifyList, credential, manifest)
            if result is True:
                print("comparing hash : True")
                hash = checkingRoot.getRoot(manifest, name).hex()
                # compare MerkleRoot
                if (hash == MerkleRoot):
                    print("checking Merkle proof : True")
                else:
                    print('checking Merkle proof : False')
            else:
                print('comparing hash : False')
            print('\n')

        #checking causal relationship
        checking_causal_relationship(verifyList, credential, manifest)

        print('\nDone!')

if __name__ == '__main__':
    verify()
