import json

class Node():
    def __init__(self, id, name, value, left, right):
        self.id = id
        self.name = name
        self.value = value
        self.left = left
        self.right = right

    def get_nodes(self, nodes):
        d = dict()

        d['id'] = self.id
        d['name'] = self.name
        d['value'] = self.value

        lchild = self.get_lchild(nodes)
        if lchild:
            d['left'] = lchild.get_nodes(nodes)
        else:
            d['left'] = None

        rchild = self.get_rchild(nodes)
        if rchild:
            d['right'] = rchild.get_nodes(nodes)
        else:
            d['right'] = None

        return d

    def get_lchild(self, nodes):
       for n in nodes:
           if n.value == self.left:
               return n

    def get_rchild(self, nodes):
        for n in nodes:
            if n.value == self.right:
                return n

    def __repr__(self):
        return self.name

class getNodes():
    def __init__(self, manifest):
        self.manifest = manifest
        self.nodes = list()

    def get_nodebyId(self, manifest, nodeId, selectDic):
        lnode = manifest['left']
        rnode = manifest['right']
        if lnode is not None and rnode is not None:
            if lnode['id'] == nodeId and lnode['name'] == selectDic[nodeId]: #selectDic[nodeId] = name
                leftNode = Node(lnode['id'], lnode['name'], lnode['value'], None, None)
                if rnode['id'] in selectDic.keys():
                    rightNode = Node(rnode['id'], rnode['name'], rnode['value'], None, None)
                else:
                    if rnode['left'] is not None and rnode['right'] is not None:
                        rightNode = Node(None, None, rnode['value'], rnode['left']['value'], rnode['right']['value'])
                    else:
                        rightNode = Node(None, None, rnode['value'], None, None)
                node = Node(None, None, manifest['value'], lnode['value'], rnode['value'])
                self.nodes.append(leftNode)
                self.nodes.append(rightNode)
                self.nodes.append(node)
                self.nodes = self.get_proofDatas(self.manifest, manifest['value'], selectDic)
                return self.nodes

            if rnode['id'] == nodeId and rnode['name'] == selectDic[nodeId]:
                rightNode = Node(rnode['id'], rnode['name'], rnode['value'], None, None)
                if lnode['id'] in selectDic.keys():
                    leftNode = Node(lnode['id'], lnode['name'], lnode['value'], None, None)
                else:
                    if lnode['left'] is not None and lnode['right'] is not None:
                        leftNode = Node(None, None, lnode['value'], lnode['left']['value'], lnode['right']['value'])
                    else:
                        leftNode = Node(None, None, lnode['value'], None, None)
                node = Node(None, None, manifest['value'], lnode['value'], rnode['value'])
                self.nodes.append(leftNode)
                self.nodes.append(rightNode)
                self.nodes.append(node)
                self.nodes = self.get_proofDatas(self.manifest, manifest['value'], selectDic)
                return self.nodes

            self.get_nodebyId(lnode, nodeId, selectDic)
            self.get_nodebyId(rnode, nodeId, selectDic)
        return self.nodes

    def get_proofDatas(self, manifest, value, selectDic):
        lnode = manifest['left']
        rnode = manifest['right']
        if lnode is not None and rnode is not None:
            leftValue = lnode['value']
            rightValue = rnode['value']
            if leftValue == value:
                if rnode['left'] is not None and rnode['right'] is not None:
                    if rnode['id'] in selectDic.keys():
                        rightNode = Node(rnode['id'], rnode['name'], rightValue, rnode['left']['value'], rnode['right']['value'])
                    else:
                        rightNode = Node(None, None, rightValue, rnode['left']['value'], rnode['right']['value'])
                else:
                    if rnode['id'] in selectDic.keys():
                        rightNode = Node(rnode['id'], rnode['name'], rightValue, None, None)
                    else:
                        rightNode = Node(None, None, rightValue, None, None)
                if manifest['name'] == "Root":
                    node = Node(None, "Root", manifest['value'], leftValue, rightValue)
                    self.nodes.append(rightNode)
                    self.nodes.append(node)
                    return self.nodes
                else:
                    node = Node(None, None, manifest['value'], leftValue, rightValue)
                    self.nodes.append(rightNode)
                    self.nodes.append(node)

                self.get_proofDatas(self.manifest, manifest['value'], selectDic)

            if rightValue == value:
                if lnode['left'] is not None and lnode['right'] is not None:
                    if lnode['id'] in selectDic.keys():
                        leftNode = Node(lnode['id'], lnode['name'], leftValue, lnode['left']['value'], lnode['right']['value'])
                    else:
                        leftNode = Node(None, None, leftValue, lnode['left']['value'], lnode['right']['value'])
                else:
                    if lnode['id'] in selectDic.keys():
                        leftNode = Node(lnode['id'], lnode['name'], leftValue, None, None)
                    else:
                        leftNode = Node(None, None, leftValue, None, None)
                if manifest['name'] == "Root":
                    node = Node(None, "Root", manifest['value'], leftValue, rightValue)
                    self.nodes.append(leftNode)
                    self.nodes.append(node)
                    return self.nodes
                else:
                    node = Node(None, None, manifest['value'], leftValue, rightValue)
                    self.nodes.append(leftNode)
                    self.nodes.append(node)

                self.get_proofDatas(self.manifest, manifest['value'], selectDic)

            self.get_proofDatas(lnode, value, selectDic)
            self.get_proofDatas(rnode, value, selectDic)
        return self.nodes

def getManifest(data, selectDic):
    if selectDic == []:
        filename = 'data\\manifest.json'
        with open(filename, 'w') as file_obj:
            json.dump(data, file_obj, indent=2)
            return

    manifest = data['manifest']
    signature = data['signature']

    nodes = getNodes(manifest)
    nodeList = list()
    for id, name in selectDic.items():
        for n in nodeList:
            if id == n.id and name == n.name:
                continue
        node = nodes.get_nodebyId(manifest, id, selectDic)
        for n in node:
            nodeList.append(n)

    dic = dict()
    root = nodeList[-1]
    manifest = root.get_nodes(nodeList)
    dic['manifest'] = manifest
    dic['signature'] = signature

    filename = 'data\\manifest.json'
    with open(filename, 'w') as file_obj:
        json.dump(dic, file_obj, indent=2)

    print("create manifest success!")

def getCredential(data, selectDic):
    credential = dict()
    credential['id'] = data['id']
    credential['issuer'] = data['issuer']
    credential['createdAt'] = data['createdAt']

    if selectDic == []:
        filename = 'data\\credential.json'
        with open(filename, 'w') as file_obj:
            json.dump(data, file_obj, indent=2)
            return

    for id in data.keys():
        if id in selectDic.keys():
            credential[id] = data[id]

    filename = 'data\\credential.json'
    with open(filename, 'w') as file_obj:
        json.dump(credential, file_obj, indent=2)

    print("create credential success!")

def getData(dic, data): #get id and name
    id = data['id']
    name = data['name']
    left = data['left']
    right = data['right']
    if id is not None and name is not None:
        dic[id] = name

    if left is not None and right is not None:
        getData(dic, left)
        getData(dic, right)

    return dic

def selectCredential():
    filename = 'credential\\credential.json'
    with open(filename) as file_obj:
        credential = json.load(file_obj)

    filename = 'credential\\manifest.json'
    with open(filename) as file_obj:
        data = json.load(file_obj)

    # check credential(id, name) in credential.json with manifest.json
    dic = dict()
    manifestDic = getData(dic, data['manifest']) #dic = {id:name}
    for id in manifestDic.keys():
        if id in credential.keys():
            continue
        else:
            print("Error: id_" + id + "does not exit in credential.json")

    index = 1
    indexDic = dict()
    for id, name in manifestDic.items():
        print("[" + str(index) + "]" + id + ": " + name)
        indexDic[index] = id + "," + name
        index += 1

    selectedNum = input("Select the credential: use comma (,) to separate the selected number[-1]Finish\n")

    if selectedNum == "-1":
        return

    numList = selectedNum.split(",")
    selectDic = dict()
    for num in numList:
        if int(num) < len(indexDic)+1:
            value = indexDic[int(num)]
            valueList = value.split(",")
            selectDic[valueList[0]] = valueList[1]
        else:
            print("Error: The selected number is incorrect!")
            return
    print("selectDic: ", selectDic)

    getCredential(credential, selectDic)
    getManifest(data, selectDic)

if __name__ == '__main__':
    selectCredential()