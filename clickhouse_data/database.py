# Data base connection script
import credentials

try: 
    from clickhouse_driver import Client
except ImportError as err:
    print('Data base library import error', err)

def client():
    """
    Function to connect to client.
    If variable client = False
    Connection will fail and provide error 
    """    
    try:   
        connection = Client(
            host=credentials.host
        )
        return connection
    except ConnectionRefusedError as err:
        print('Error \n' + err)
        return
    
def execute_query(query):
    try:
        db_query = client().execute(query)
        return db_query
    except ConnectionRefusedError as err:
        print('Error \n' + err)
        return       