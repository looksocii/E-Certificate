from Service_App.verify_credential.checkingMerkleProof import checkingMerkleProof
from Service_App.verify_credential.comparingHash import comparingHash
from Service_App.verify_credential.checkingCausalRelationship import checking_causal_relationship
from Service_App.verify_credential.getVerifyData import *
import time, json, logging
from urllib.request import urlopen

logger = logging.getLogger(__name__)

def h2b(data):
    if data:
        return bytearray.fromhex(data)

def get_timestamp(datetime):
    timeArray = time.strptime(datetime, '%Y-%m-%dT%H:%M:%S:%fZ')
    timestamp = time.mktime(timeArray)
    return timestamp

def issuer_verify(txid, issuer):
    # verify issuer authenticity
    # compare issuer's address in issuer.json with blockchain sender's address
    bol = False
    #sender = 'mtmixin9kfZXRMaPfbeS9gHxC1nVMwudtR'
    sender = get_issuerAddress(txid)
    
    """
    url = issuer['url']
    logger.info('url %s' % url)
    response = urlopen(url)
    issuer_data = json.load(response)
     addressList = issuer_data['addressList']
     for addressInfo in addressList:
        issuer_addr = addressInfo['address']
        if issuer_addr == sender:
            # check date True if (issue date > created)
            create_timestamp = get_timestamp(addressInfo['created'])
            issue_timestamp = get_timestamp(credential['createdAt'])
            if create_timestamp < issue_timestamp:
                bol = True
                return bol
            else:
                return bol
    """

    if 'mtmixin9kfZXRMaPfbeS9gHxC1nVMwudtR' == sender:
        # check date True if (issue date > created)
        bol = True
        return bol
    else:
        return bol

def verifyCredential():
    data_path = 'Service_App/verify_credential/data'
    credential_path = data_path + '/credential'

    #with open(data_path + '/manifest.json') as file_obj:
    with open(data_path + '/manifest.json') as file_obj:
        data = json.load(file_obj)
    manifest = data['manifest']
    signature = data['signature']
    txid = signature['txId']

    result_list = list()

    with open(data_path + '/issuer.json') as file_obj:
        issuer = json.load(file_obj)
    issuer_result = issuer_verify(txid, issuer)

    if issuer_result:
        result_list.append({'issuer_authenticity' : True})
        #get MerkleRoot from blockchain
        MerkleRoot = '0x01' + get_merkleRoot(txid)

        # get selected credential's name
        checkingRoot = checkingMerkleProof(manifest)
        verifyList = list(set(checkingRoot.getVerifyList(manifest)))

        #comparing hash and checking merkle proof
        for name in verifyList:
            result_list.append({'credential_name' :  name})
            print(name)
            # rew comment
            result = comparingHash(name, verifyList, credential_path, manifest)
            if result:
                result_list.append({'comparing_hash' : True})
                hash = checkingRoot.getRoot(manifest, name)
                # compare MerkleRoot
                if (hash == MerkleRoot):
                    result_list.append({'checking_Merkle_proof' : True})
                else:
                    result_list.append({'checking_Merkle_proof' : False})
            else:
                result_list.append({'comparing_hash' : False})

        #checking causal relationship
        relationship_list = checking_causal_relationship(verifyList, credential_path, manifest)
        for result in relationship_list:
            result_list.append(result)

    else:
        result_list.append({'issuer_authenticity' : False})
    return result_list

if __name__ == '__main__':
    verifyCredential()
