# Data base connection script
import credentials

try: 
    from clickhouse_driver import Client
except ImportError as err:
    print('Data base library import error', err)

client = Client(host=credentials.host)    

def execute_query(query):
    try:
        return client.execute(query)        
    except ConnectionRefusedError as err:
        print('Error \n' + err)
        return