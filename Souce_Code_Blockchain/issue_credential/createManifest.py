import json
from merkletree import MerkleTree
from merkletools import MerkleTools, Node
from getFileName import file_name
from createCredential import Credential
from collections import OrderedDict

mTools = MerkleTools()
mTree = MerkleTree()

class Manifest():
    def __init__(self): #clr_data = dic (return from get_credential)
        self.dic = OrderedDict()  # { parentId:[childsId] }
        self.nodes = list()  # all nodes for individual (include openbadge and clr)
        self.idList = list()

    def get_association(self, data): #data = tree\student_*.json
        credentialList = list()
        dic = OrderedDict() #dic[parentName] = childList
        for index, value in enumerate(data['credentialTree']):
            print("[" + str(index) + "]" + value['name'])
            credentialList.append(value)

        while(True):
            credentialNum = int(input("Select the credential as ParentCredential: \n[-1]Finish\n"))
            if credentialNum == -1:
                break
            if credentialNum < len(credentialList):
                childList = list()
                print("select : " + credentialList[credentialNum]['name'])
                while (True):
                    subNum = int(input("Select the sub-credential of \'" + credentialList[credentialNum]['name'] + "\'\n[-1]Finish\n"))
                    if subNum == -1:
                        data['credentialTree'][credentialNum]['child'] = childList
                        name = data['credentialTree'][credentialNum]['name']
                        dic[name] = childList
                        break
                    if subNum < len(credentialList):
                        if subNum == credentialNum:
                            print("Error: credential and sub-credential cannot be the same file")
                        else:
                            print("select : " + credentialList[subNum]['name'])
                            childList.append(credentialList[subNum]['name'])
                    else:
                        print("invalid number!")
            else:
                print("invalid number!")

        return dic  #dic[parentName] = childList

    def get_credentialAssociation(self):
        num = int(input("Credential Association : [1]For all students [2]For each student [-1]Cancel\n"))

        root, dir, files = file_name('tree')
        #for all students
        if num == 1:
            print("For all student")
            with open('tree\\' + files[0]) as file_obj:
                data = json.load(file_obj)
            dic = self.get_association(data)  #dic[parentName] = childList

            dicKey = list()
            for key in dic.keys():
                dicKey.append(key)

            for file in files:
                with open('tree\\' + file) as file_obj:
                    data = json.load(file_obj)
                for value in data['credentialTree']:
                    name = value['name']
                    if name in dicKey:
                        value['child'] = dic[name] #add name's childList to child
                # write data back to tree
                    filename = 'tree\\' + file
                    with open(filename, 'w') as file_obj:
                        json.dump(data, file_obj, indent=2)
        #for each student
        if num == 2:
            print("For each student")
            for file in files:
                with open('tree\\' + file) as file_obj:
                    data = json.load(file_obj)
                dic = self.get_association(data)
                for value in data['credentialTree']:
                    name = value['name']
                    if name in dic.keys():
                        value['child'] = dic[name] #add name's childList to child
                #write data back to tree
                filename = 'tree\\' + file
                with open(filename, 'w') as file_obj:
                    json.dump(data, file_obj, indent=2)

        if num == -1:
            return

    #get the first level of the tree
    def get_treeRoot(self, data): #data = tree\student_*.json
        child_list = list() #list of the child
        root_list = list()  #list of the root id (parentId)
        for value in data['credentialTree']:
            if len(value['child']) > 0:
                for v in value['child']:
                    child_list.append(v) #add all of the child to child_list

        for value in data['credentialTree']:
            if value['name'] in child_list:
                continue
            else:
                root_list.append(value['id'])
        return root_list

    #add child node (child's full data) to childList not only name
    def get_treeNode(self, data):#data = tree\student_*.json
        treeNodes = list()
        for credential in data['credentialTree']:
            if len(credential['child']) > 0:
                childList = list()  #add child node to childList not only name
                for child in credential['child']:
                    for childData in data['credentialTree']:
                        if child == childData['name']:
                            childList.append(childData)
                credential['child'] = childList
                treeNodes.append(credential)
            else:
                treeNodes.append(credential)
        return treeNodes

    # parentCredential and childCredential cannot be the same file,
    # get id list and then convert list to set, if len(set) != len(list), error occur
    def getIdList(self, parentNode):
        childNodes = parentNode['child']
        if len(childNodes) > 0:
            for childNode in childNodes:
                self.idList.append(childNode['id'])
                name = childNode['name']
                idSet = set(self.idList)
                if len(idSet) < len(self.idList):
                    print('Error: \'' + name + '\' parent credential and child credential cannot be the same file!')
                    self.idList[0] = 'error'
                    return self.idList
                self.getIdList(childNode)
        return self.idList

    #add child node (Cyclic traversal)
    def get_treeAddChild(self, treeNodes):
        for parentNode in treeNodes:
            childNodes = parentNode['child']
            if len(childNodes) == 0:
                continue
            for childNode in childNodes:
                for treeNode in treeNodes:
                    if childNode['id'] == treeNode['id']:
                        if len(treeNode['child']) == 0:
                            continue
                        childList = list()
                        for child in treeNode['child']:
                            childList.append(child)
                        childNode['child'] = childList
            # parentCredential and childCredential cannot be the same file,
            # compare parentId with chileId
            self.idList.append(parentNode['id'])
            name = parentNode['name']
            idList = self.getIdList(parentNode)
            idSet = set(idList)
            if idList[0] == 'error':
                treeNodes = None
                return treeNodes
            else:
                if len(idSet) < len(idList):
                    print('Error: \'' + name + '\' parent credential and child credential cannot be the same file!')
                    treeNodes = None
                    return treeNodes
                else:
                    #reset self.idList
                    self.idList = list()
                    #Cyclic traversal child node
                    self.get_treeAddChild(childNodes)
        return treeNodes

    #get the root node of the tree
    def get_treeRootNodes(self, treeRoot, treeNodes):
        nodes = list()
        treeNodes = self.get_treeAddChild(treeNodes)
        for rootNode in treeRoot:
            for node in treeNodes:
                if rootNode == node['id']:
                    nodes.append(node)
        return nodes

    #self.dic[parentId] = childDic (childId : childValue)
    def get_nodesDic(self, treeRootNodes):
        for node in treeRootNodes:
            childNodes = node['child']
            if len(childNodes) > 0:
                childDic = OrderedDict()
                for child in childNodes:
                    childDic[child['id']] = child['targetHash']
                    self.dic[node['id']] = childDic
                self.get_nodesDic(childNodes)
        return self.dic

    #get evidence node
    def get_nodesEvidence(self, treeRootNodes):
        nodesDic = self.get_nodesDic(treeRootNodes)
        dicKeyList = list()
        nodesList = list()
        for key in nodesDic.keys():
            nodesList.append(key)  # key = id

        nodesList.reverse()
        #print("nodesList_reverse :", nodesList)

        for node in nodesList:
            childDic = nodesDic[node] #nodesDic[node] = childId : chlidValue
            childList = list()
            evidenceList = list()
            for key in childDic.keys():
                child = childDic[key]
                key_evidence = key + "_evidence"
                for key in self.dic.keys():
                    dicKeyList.append(key)
                if key_evidence in dicKeyList:
                    evidenceList.append(self.dic[key_evidence]) #evidence = leftChild,
                    evidenceList.append(child)#child = rightChild
                else:
                    childList.append(child) #leafNode

            #append childList to evidenceList
            for child in childList:
                evidenceList.append(child)
            #print("evidenceList :", evidenceList)
            if len(evidenceList) > 1:
                root = mTree.getMerkleTreeByHash(evidenceList)
            else:
                root = mTree.getMerkleTreeByHash([evidenceList[0], evidenceList[0]])

            evidence = root[-1].value
            # print("evidence :", evidence)
            self.dic[node + "_evidence"] = evidence
            for node in root:
                self.nodes.append(node)  # to build MerkleTree
        """
        for node in self.nodes:
            print("value :", node.value)
        """

        return self.dic, self.nodes

    #get full nodes
    def get_nodes(self, treeRootNodes):
        self.dic, self.nodes = self.get_nodesEvidence(treeRootNodes)
        dicKeyList = list()
        for key in self.dic.keys():
            dicKeyList.append(key)

        evidenceList = list()
        nodeList = list()
        for node in treeRootNodes:
            node_evidence = node['id'] + "_evidence"
            targetHash = node['targetHash']
            if node_evidence in dicKeyList:
                evidenceList.append(self.dic[node_evidence]) #leftChild
                evidenceList.append(targetHash)#rightChild
            else:
                nodeList.append(targetHash)#leafNode

        # append childList to evidenceList
        for node in nodeList:
            evidenceList.append(node)
        #print("evidenceList :", evidenceList)
        if len(evidenceList) > 1:
            root = mTree.getMerkleTreeByHash(evidenceList)
        else:
            root = mTree.getMerkleTreeByHash([evidenceList[0], evidenceList[0]])

        # evidence = root[-1].value
        # print("evidence :", evidence)
        for node in root:
            self.nodes.append(node)  # to build MerkleTree

        return self.nodes

    #using full nodes to build the MerkleTree
    def get_MerkleTree(self, treeRootNodes, data):#data = tree\student_*.json
        self.nodes = self.get_nodes(treeRootNodes)
        valueList = list()
        for value in data['credentialTree']:
            valueList.append(value['targetHash'])

        #add 'id' and 'name' to manifest (merkleProof)
        for node in self.nodes:
            value = node.value
            if value in valueList:
                for credential in data['credentialTree']:
                    if value == credential['targetHash']:
                        node.id = credential['id']
                        node.name = credential['name']

        root = self.nodes[-1]
        merkleTree = root.get_nodes(self.nodes)

        return merkleTree

    #create manifest
    def create(self):
        self.get_credentialAssociation()

        root, dir, files = file_name('tree')
        for file in files:
            with open('tree\\' + file) as file_obj:
                data = json.load(file_obj)
            treeRoot = self.get_treeRoot(data)
            treeNodes = self.get_treeNode(data)
            treeRootNodes = self.get_treeRootNodes(treeRoot, treeNodes)
            merkleTree = self.get_MerkleTree(treeRootNodes, data)

            # write an individual credential and manifest to 'data' dir
            file_path = 'data\\' + str(file).split(".json")[0]
            filename = file_path + '\\' + 'manifest.json'
            dic = OrderedDict()
            dic['manifest'] = merkleTree
            dic['signature'] = OrderedDict()
            dic['signature']['txId'] = ""
            dic['signature']['type'] = "BTCOpReturn"
            dic['signature']['chain'] = ""
            with open(filename, 'w') as file_obj:
                json.dump(dic, file_obj, indent=2)

            #reset self.dic and self.nodes
            self.dic = OrderedDict()
            self.nodes = list()

        print("create manifest success!")

class AggregateCredential():
    def __init__(self):
        self.RootList = list()
        self.file_dir = 'data'
        self.root, self.dirs, self.files = file_name(self.file_dir)
        self.manifest = OrderedDict()

    def get_node(self, id, name, value, left, right):
        dic = OrderedDict()
        dic['id'] = id
        dic['name'] = name
        dic['value'] = value
        dic['left'] = left
        dic['right'] = right
        return dic

    # hex to binary
    def h2b(self, data):
        if data:
            return bytearray.fromhex(data)

    def get_individualRoot(self):
        if len(self.dirs) > 1:
            for dirs in self.dirs:
                with open(self.file_dir + '\\' + dirs + '\\manifest.json') as file_obj:
                    data = json.load(file_obj)
                data['manifest']['name'] = None
                value = data['manifest']['value']
                self.RootList.append(value)
        else:
            with open(self.file_dir + '\\' + self.dirs[0] + '\\manifest.json') as file_obj:
                data = json.load(file_obj)
            data['manifest']['name'] = 'Root'
            #write back to manifest.json with name 'Root'
            filename = self.file_dir + '\\' + self.dirs[0] + '\\manifest.json'
            with open(filename, 'w') as file_obj:
                json.dump(data, file_obj, indent=2)

    def addProof2manifest(self):
        self.get_individualRoot()
        if len(self.RootList) > 0:
            mTools.add_leaf(self.RootList)
            mTools.make_tree()
            for dirs in self.dirs:
                self.manifest = OrderedDict()
                with open(self.file_dir + '\\' + dirs + '\\manifest.json') as file_obj:
                    data = json.load(file_obj)
                self.manifest = data['manifest']
                signature = data['signature']
                index = self.dirs.index(dirs)
                proof = mTools.get_proof(index)
                root = mTools.get_merkle_root()
                manifestDic = OrderedDict()
                for p in proof:
                    for key in p.keys():
                        if key == "left":
                            manifestDic['id'] = None
                            manifestDic['name'] = None
                            manifestDic['value'] = mTools.getHash_hex(self.h2b(p[key]) + self.h2b(self.manifest['value']))
                            manifestDic['left'] = self.get_node(None, None, p[key], None, None)
                            manifestDic['right'] = self.manifest
                            self.manifest = self.get_node(None, None, manifestDic['value'], manifestDic['left'],
                                                     manifestDic['right'])
                            continue
                        if key == "right":
                            manifestDic['id'] = None
                            manifestDic['name'] = None
                            manifestDic['value'] = mTools.getHash_hex(self.h2b(self.manifest['value']) + self.h2b(p[key]))
                            manifestDic['left'] = self.manifest
                            manifestDic['right'] = self.get_node(None, None, p[key], None, None)
                            self.manifest = self.get_node(None, None, manifestDic['value'], manifestDic['left'],
                                                     manifestDic['right'])
                            continue

                manifestDic['id'] = None
                manifestDic['name'] = "Root"
                manifestDic['value'] = root
                manifestDic['left'] = self.manifest['left']
                manifestDic['right'] = self.manifest['right']

                dic = OrderedDict()
                dic['manifest'] = manifestDic
                dic['signature'] = signature
                #add aggregate proof back to individual manifest.json
                filename = self.file_dir + '\\' + dirs + '\\manifest.json'
                with open(filename, 'w') as file_obj:
                    json.dump(dic, file_obj, indent=2)

def main():
    credential = Credential()
    credential.create()

    manifest = Manifest()
    manifest.create()

    aggregateCredential = AggregateCredential()
    aggregateCredential.addProof2manifest()

if __name__ == '__main__':
    main()
