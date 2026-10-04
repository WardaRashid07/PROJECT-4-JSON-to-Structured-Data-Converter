from config import CONTENT , CONFIG
import logging

logging.basicConfig(level= "INFO", format = '%(asctime)s | %(levelname)s | %(message)s')
logger =logging.getLogger()

if CONFIG == 'json':
    print(" proceeding a json file ")
else:
    print(" procceding a ndjson file")

set_check=set()

def inspect_recs(cont):
    count_mal = 0
    contents = []
    for i,element in enumerate(cont):
        if not  isinstance(element,dict) or not element or 'id' not in element:
            # print(f" malformed element = {element}, skipping..")
            # logger.warning("malformed element at %d the element itself is = %s",i,element)
            count_mal+=1
            continue
        # if i ==0 :
        # print(f"the element is = " ,element )
        contents.append(element)
        for key, value in element.items():
             # print( "key is = " , key)
             # print("the type is = ", type(value))
             # set_check.add(key)
             if isinstance(value,dict):
                 # print(f"this  is a dict = {key}")
                 for key1,value1 in value.items():
                     pass
                     # print(" its key is  =   " ,key1)
                     # print("the type is = ", type(value1))
    return count_mal,contents

def flatten(d, prefix=""):
    result = {}
    for key, value in d.items():
        if prefix:
            new_key = prefix + "__" + key
        else:
            new_key = key

        if isinstance(value, dict):
            result.update(flatten(value, new_key))
        elif isinstance(value, list):
            result[new_key] = "|".join(value)
            set_check.add(new_key)
        else:
            set_check.add(new_key)
            result[new_key] = value

    return result



count_mal, contents = inspect_recs(CONTENT)

flattened_records = []
for record in contents:
    flattened_records.append(flatten(record))
print(" the values in set  are = ",set_check, "and count of malformed is = " ,count_mal)
# print("flattened records" , flattened_records)
