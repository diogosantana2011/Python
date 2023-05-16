# Script to format data fetched
# Implementation to format data
# Data to be fetched and saved to a JSON file first# Call on data
import database
from datetime import date

client = database.client()

print(
    client.execute('SHOW DATABASES'),
    client.execute('SELECT * FROM system.numbers LIMIT 20'+ '\n'),
    client.execute(
        'SELECT %(date)s, %(a)s + %(b)s ',
        {'date': date.today(), 'a': 1, 'b': 2}
    ),
    client.execute(
        "c",
        {'myvar': 1}
    ),
)

# INSERT
# test_insert = client.execute(
#     'INSERT INTO system (x) VALUES (%(a)s), (%(b)s), (%(c)s),',
#     {'a': 1, 'b': 2, 'c': 3}
# )
# print(test_insert)