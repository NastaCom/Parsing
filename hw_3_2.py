from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['hh']
search_collection = db['search']

salary = float(input("Введите значение зарплаты: "))

def search_vacantion_salary(collection):
    for item in collection.find({'$or': [{'salary_min': {'$gt': salary}},
                                 {'salary_min': 'None', 'salary_max': {'$gt': salary}}]
                         }):
        pprint(item)

search_vacantion_salary(search_collection)
