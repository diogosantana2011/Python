from pymongo import ASCENDING
import config, pymongo, datetime, os, logging, logging.handlers

# MONGO CONNECTION

#
# TODO: 
# FIX OBJECT CREATION DB;
# INSTEAD OF VARIOUS DB_TRACES
# ADD 1 WITH OPERATION RESULT vs CURRENT 7!!
# 

my_client = pymongo.MongoClient(config.mongo_url)
mydb = my_client[config.mongo_client]
db_list = my_client.list_database_names()
mycol = mydb[config.mongo_metrics_col]
collist = mydb.list_collection_names()
log_collection = mydb.log
log_collection.create_index([('timestamp', ASCENDING)])

def db_trace(msg, operation):
    '''Log `msg + operation` to MongoDB Log'''
    entry ={}
    entry['timestamp'] = datetime.datetime.utcnow()
    entry['msg'] = msg
    entry['operation'] = operation
    log_collection.insert_one(entry)

def checkIsDir():
    ''' Checks if Logs directory exists before script runs.'''
    path = os.getcwd()
    logs_folder = '/logs'
    created_logs_folder = path + logs_folder
    
    if not os.path.isdir(created_logs_folder):
        os.makedirs(created_logs_folder, mode=0o777, exist_ok=False)
        print('Logs folder has been created.')
        logging.info('Logs folder has been created.')
        db_trace(f'Folder {created_logs_folder} has been created', 'Logs folder created')
    elif os.path.isdir(created_logs_folder):
        print('Logs folder already exists.')
        logging.info('Logs folder already exists! Writting in existing file!')
        db_trace('Logs folder already exists. Writting in existing file', 'Check if DB Existing')  