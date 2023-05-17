# Script to format data fetched
# Implementation to format data
# Data to be fetched and saved to a JSON file first# Call on data
import database
from datetime import date

client = database.client()
collection = 'system'

print(
    # database.execute_query('SHOW DATABASES'),
    # database.execute_query('SELECT * FROM system.numbers LIMIT 20'+ '\n'),
    # database.execute_query(
    #     'SELECT %(date)s, %(a)s + %(b)s ',
    #     {'date': date.today(), 'a': 1, 'b': 2}
    # ),
    # client.execute(
    #     "c",
    #     {'myvar': 1}
    # ),
    # database.execute_query(f'USE {collection}'),
    # database.execute_query("SHOW DATABASES LIKE '%de%'"),
    # database.execute_query("SHOW DATABASES NOT LIKE '%de%'"),
    # database.execute_query("SHOW TABLES FROM system LIKE '%user%'"),
    # database.execute_query("SHOW TABLES FROM system ILIKE '%USER%'"),
    # database.execute_query("SHOW TABLES FROM system NOT LIKE '%s%'"),
    # database.execute_query("SHOW TABLES FROM system LIMIT 2")
    # database.execute_query('SHOW COLUMNS FROM aggregate_function_combinators') # Returns empty list []
)

# INSERT
# test_insert = database.execute_query(
#     'INSERT INTO system (x) VALUES (%(a)s), (%(b)s), (%(c)s),',
#     {'a': 1, 'b': 2, 'c': 3}
# )
# print(test_insert)