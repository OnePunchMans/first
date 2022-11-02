import macd
import kzz
import rule

import pandas
import pymongo

# pymongofrom pymongo import MongoClient
# db = MongoClient().get_database('day')
#
# data = pandas.DataFrame(db.get_collection('601677').find().sort('dat',pymongo.DESCENDING))
# print()
# print(data['close'])
# macd.macd(data['close'])
rule.sandielang()