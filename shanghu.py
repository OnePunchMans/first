import cx_Oracle as ora
import requests
import pandas as pd
from pymongo import MongoClient
import csv

from sqlalchemy import create_engine


#engine = create_engine('oracle+cx_oracle:batch')



conn = ora.connect('batch/Sd_Batch*37@10.161.246.2:10001/znpt')
df = pd.read_sql('select * from temp_shanghu3',con=conn)
print(df.count())

