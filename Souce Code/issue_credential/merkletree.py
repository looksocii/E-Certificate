from merkletools import MerkleTools

class MerkleTree(object):
    def getMerkleTreeByData(self, datas):
        mt = MerkleTools()
        mt.add_leaf(datas, True)
        mt.make_tree()

        nodes = mt.getNodes()
        return nodes

    def getMerkleTree(self, hash, data):
        mt = MerkleTools()
        mt.add_leaf(hash)
        mt.add_leaf(data, True)
        mt.make_tree()

        nodes = mt.getNodes()
        return nodes

    def getMerkleTreeByHash(self, hash_datas):
        mt = MerkleTools()
        mt.add_leaf(hash_datas)
        mt.make_tree()

        nodes = mt.getNodes()
        return nodes

def main():
    mt = MerkleTree()
    nodes = mt.getMerkleTree(["111", "222"])
    #datas = mt.getMerkleTreeHash("f6e0a1e2ac41945a9aa7ff8a8aaa0cebc12a3bcc981a929ad5cf810a090e11ae", "222")
    #datas = mt.getMerkleHash("f6e0a1e2ac41945a9aa7ff8a8aaa0cebc12a3bcc981a929ad5cf810a090e11ae", "9b871512327c09ce91dd649b3f96a63b7408ef267c8cc5710114e629730cb61f")
    for node in nodes:
        print("name :", node.name)
        print("value :", node.value)
        print("left :", node.left)
        print("right :", node.right)

if __name__ == '__main__':
    main()
