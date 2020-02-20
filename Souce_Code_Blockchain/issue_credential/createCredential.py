import json
from merkletools import MerkleTools
from getFileName import file_name
import uuid
import os
import datetime
from collections import OrderedDict

mTools = MerkleTools()

class Credential():
    def get_uuid(self):
        return 'urn:uuid:' + str(uuid.uuid4())

    def create(self):
        """
        credential.json
        "id":"",
        "issuer":"",
        "urn:uuid:id#1":"credential#1.json"
        "urn:uuid:id#2":"credential#2.json"
        .....
        """
        dic = OrderedDict()
        dic['id'] = self.get_uuid()
        with open('issuer.json') as file_obj:
            issuer = json.load(file_obj)

        dic['issuer'] = issuer
        dic['issuer']['id'] = self.get_uuid()
        createdAt = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S:%fZ')
        dic['createdAt'] = createdAt

        credential_dir = 'credential'
        croot, cdirs, cfiles = file_name(credential_dir)

        issuerStr = ""
        for key in issuer.keys():
            issuerStr += issuer[key]

        for dirs in cdirs:  # cdirs = 'credential dir' , dirs = for each student
            root, dir, files = file_name(credential_dir + '\\' + dirs)
            assocList = list()
            for file in files:  # file = all individual credential under the dirs
                assocDic = OrderedDict()
                with open('credential\\' + dirs + '\\' + file) as file_obj:
                    data = json.load(file_obj)
                uuid = self.get_uuid()
                dic[uuid] = data

                assocDic['id'] = uuid
                assocDic['name'] = file
                dataStr = dic['id'] + issuerStr + str(createdAt) + str(data)
                #print(file + ": " + dataStr)
                assocDic['targetHash'] = mTools.getHash_hex(dataStr.encode('utf-8'))
                assocDic['child'] = list()
                assocList.append(assocDic)

            folderName = str(os.path.split(root)[-1])
            #create credential
            file_path = 'data\\' + folderName
            if os.path.isdir(file_path):
                pass
            else:
                os.mkdir(file_path)

            filename = file_path + '\\' + 'credential.json'
            with open(filename, 'w') as file_obj:
                json.dump(dic, file_obj, indent=2)

            #create_tree (association)
            tree = OrderedDict()
            tree['credentialTree'] = assocList
            filename = 'tree\\' + folderName + '.json'
            with open(filename, 'w') as file_obj:
                json.dump(tree, file_obj, indent=2)

def main():
    credential = Credential()
    credential.create()

if __name__ == '__main__':
    main()





