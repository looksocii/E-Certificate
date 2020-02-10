class ChildNode():
    def __init__(self, manifestData):
        self.hash = None
        self.root = manifestData['value']
        self.manifest_data = manifestData

    def getRoot(self, name, evidence, manifestData):
        lnode = manifestData['left']
        rnode = manifestData['right']
        if lnode is not None and rnode is not None:
            if lnode['name'] == name or rnode['name'] == name:
                self.hash = manifestData['value']
                if self.hash == evidence:
                    return self.hash
                self.hash = self.getRootbyValue(self.hash, evidence, self.manifest_data)
                return self.hash
            self.getRoot(name, evidence, lnode)
            self.getRoot(name, evidence, rnode)
            return self.hash

    def getRootbyValue(self, value, evidence, manifestData):
        lnode = manifestData['left']
        rnode = manifestData['right']
        if lnode is not None and rnode is not None:
            if lnode['value'] == value or rnode['value'] == value:
                self.hash = manifestData['value']
                if self.hash == evidence:
                    return self.hash
                self.getRootbyValue(self.hash, evidence, self.manifest_data)
            self.getRootbyValue(value, evidence, lnode)
            self.getRootbyValue(value, evidence, rnode)
            return self.hash

class Evidence():
    def __init__(self):
        self.evidence = None

    def getEvidence(self, name, manifestData):
        lnode = manifestData['left']
        rnode = manifestData['right']
        if lnode is not None and rnode is not None:
            if lnode['name'] == name:
                self.evidence = rnode['value']
                return self.evidence
            if rnode['name'] == name:
                self.evidence = lnode['value']
                return self.evidence
            self.getEvidence(name, lnode)
            self.getEvidence(name, rnode)
        return self.evidence

#get credential's id
def get_idList(credentialData):
    idList = list()
    for key in credentialData.keys():
        if key == 'id' or key == 'issuer' or key == 'createdAt':
            continue
        idList.append(key)
    return idList

def getChildList(parentName, evidenceValue, ChildNode, verifyList, manifestData):
    childList = list()
    for childName in verifyList.values():
        childRoot = ChildNode.getRoot(childName, evidenceValue, manifestData)
        if childRoot == evidenceValue:
            childList.append(childName)
    return childList

def checking_causal_relationship(verifyList, credentialData, manifestData):
    idList = get_idList(credentialData)
    for id in verifyList.keys():
        idList.append(id)
    idSet = set(idList)
    if len(idSet) == len(verifyList):
        child = ChildNode(manifestData)
        evidence = Evidence()
        leafNodes = list()
        for parentName in verifyList.values():
            # get the evidence of the parentNode
            evidenceValue = evidence.getEvidence(parentName, manifestData)
            if evidenceValue is not None:
                childs = getChildList(parentName, evidenceValue, child, verifyList, manifestData)
                if len(childs) > 0:
                    print(str(childs) + ' is part of the \'' + parentName + '\'')
                else:
                    leafNodes.append(parentName)
        if len(leafNodes) > 1:
            print(str(leafNodes) + " are leaf node")
        else:
            print(str(leafNodes) + " is leaf node")