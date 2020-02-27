import json

def Writejson():
    listed = {"name" : "61070133", "parent_Node": "Math", "child_Node" : ["std1.pdf", "std2.pdf"]}
    jsondata = json.dumps(listed)
    print(jsondata)
    f = open("index2.json", "w+")
    f.write(jsondata)
    f.close()
Writejson()
