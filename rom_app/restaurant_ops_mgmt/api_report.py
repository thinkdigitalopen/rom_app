import frappe
from datetime import datetime
import json


def get_conditions(filters):
    print('get_conditions')
    print(filters)
    print(type(filters))
    if (type(filters) is str):
        filters = json.loads(filters)

    print(type(filters))
    print(filters)

    conditions = {}
    for key, value in filters.items():
        print('_________________inside loop________________')
        print(key)
        print(value)
        if filters.get(key):
            conditions[key] = value

    print("result of get_conditions")
    print(conditions)
    print(type(conditions))
    return conditions
