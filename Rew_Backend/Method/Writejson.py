import json

def Writejson(Node):
    listed = {"name" : "61070133", "parent_Node": "Math", "child_Node" : ["std1.pdf", "std2.pdf"]}
    jsondata = json.dumps(Node)
    print(jsondata)
    f = open("index.json", "w+")
    f.write(jsondata)
    f.close()
Writejson()
