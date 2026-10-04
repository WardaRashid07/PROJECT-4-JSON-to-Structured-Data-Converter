import json


CONFIG=None
path = r"C:\Users\warda\Downloads\records.ndjson"
path2 = r"C:\Users\warda\Downloads\records.json"
CONTENT=[]
def loading(paths,configure):
    with open(paths) as file:

        try :
            contentt = json.load(file)
            print(" the file is a json obj " , contentt)
            configure='JSON'
            for i,line in enumerate(contentt) :
                if i <= 5:
                    pass
                    # print(f"pinting line {i}, {line}")


        except json.JSONDecodeError:
            configure='NDJSON'
            file.seek(0)
            contentt=[]
            print(" the file was a .ndjson ")
            for i,line in enumerate(file) :
               cont = json.loads(line)
               contentt.append(cont)
               if i   <=5 :
                   pass
                   # print(f"pinting line {i}, {cont}")
    return configure,contentt
CONFIG, CONTENT = loading(path,CONFIG)
