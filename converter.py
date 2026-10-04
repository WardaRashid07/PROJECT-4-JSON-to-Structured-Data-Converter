from importlib.resources import contents
import pandas as pd
import pyarrow
import numpy as np
from config import CONTENT , CONFIG
import logging

from flattener import flattened_records,set_check,count_mal


logging.basicConfig(level= "INFO", format = '%(asctime)s | %(levelname)s | %(message)s')
logger =logging.getLogger()




def backfill_missing_keys(records):
    for record in records :
        for key in set_check:
            if key not in record :
                record[key] = None
    return records




records = backfill_missing_keys(flattened_records)
df = pd.DataFrame(records)
df.to_parquet( "output.parquet", index =False)
df.to_csv("out_put.csv", index=False)

logger.info(f"Total Records = {len(CONTENT) }  Successfull loads = {len(records)}  Skipped/failed = {count_mal}")