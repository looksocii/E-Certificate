from merkletools import MerkleTools

class TargetHash():
    def __init__(self):
        self.targetHash = None

    def getTargetHash(self, nodeName, manifestData):
        name = manifestData['name']
        value = manifestData['value']
        lnode = manifestData['left']
        rnode = manifestData['right']
        if name == nodeName:
            self.targetHash = value
            return self.targetHash
        if lnode is not None and rnode is not None:
            self.getTargetHash(nodeName, lnode)
            self.getTargetHash(nodeName, rnode)
        return self.targetHash

def getCredential(id, credentialData):
    credentialId = credentialData['id']
    issuer = credentialData['issuer']
    issuerStr = ""
    for key in issuer.keys():
        issuerStr += issuer[key]
    createdAt = credentialData['createdAt']
    data = str(credentialData[id]) #credential data

    credential = credentialId + issuerStr + createdAt + str(data)
    #print('getCredential: ', credential)
    return credential

def comparingHash(id, name, verifyList, credentialData, manifestData):
    mt = MerkleTools()
    result = False
    targetHash = TargetHash().getTargetHash(name, manifestData)
    #print('targetHash: ', targetHash)
    if id in verifyList.keys():
        credential = getCredential(id, credentialData)
        credentialHash = mt.getHash_hex(credential.encode('utf-8'))
        #print('credentialHash: ', credentialHash)
        if credentialHash == targetHash:
            result = True
    return result




