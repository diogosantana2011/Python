#
# Admin Metrics API data
# Get login values for all and add them = result
#

from genericpath import exists
import requests
import json
import datetime, os
from pathlib import Path
import logging , logging.handlers 


# ADD LOGS TO MONGO DB VS .LOG FILES
import pymongo
from pymongo import ASCENDING

# MONGO CONNECTION
my_client = pymongo.MongoClient('mongodb://localhost:27017')
mydb = my_client['diogo_metrics-scripts-logs']
db_list = my_client.list_database_names()

if 'mydatabase' in db_list:
    print('Database exists!')
    logging.info('Database already exists!')
    
mycol = mydb['metrics_logs']
collist = mydb.list_collection_names()
if 'metrics_logs' in collist:
    print("The collection exists.")
    logging.info('Collection already exists!')
    
log_collection = mydb.log
log_collection.create_index([('timestamp', ASCENDING)])

def log(msg, operation):
    '''Log `msg + operation` to MongoDB Log'''
    entry ={}
    entry['timestamp'] = datetime.datetime.utcnow()
    entry['msg'] = msg
    
    # MAKE 'OPERATION' OBJECT CONTAINING INFORMATION VS DUPLICATE ENTRIES
    # https://github.com/log4mongo/log4mongo-python
    entry['operation'] = operation
    log_collection.insert_one(entry)
        
def main(): 
    # LOGGING
    fmtstr = '%(asctime)s: %(levelname)s: %(funcName)s: Line: %(lineno)d %(message)s' 
    datestr = '%d/%m/%Y %I:%M:%S %p'
    logging.basicConfig(
        level=logging.DEBUG,
        filename='logs/operation_output.log', 
        filemode='w+',
        format=fmtstr,
        datefmt=datestr
    )
    path = os.getcwd()
    logs_folder = '/logs'
    created_logs_folder = path + logs_folder
    
    if not os.path.isdir(created_logs_folder):
        os.makedirs(created_logs_folder, mode=0o777, exist_ok=False)
        print('Logs folder has been created.')
        logging.info('Logs folder has been created.')
        log(f'Folder {created_logs_folder} has been created', 'Logs folder created')
    elif os.path.isdir(created_logs_folder):
        print('Logs folder already exists.')
        logging.info('Logs folder already exists! Writting in existing file!')
        log('Logs folder already exists. Writting in existing file', 'Check if DB Existing')
        
    while True:
        try:            
            # DATE INPUTS
            date = input('Enter an startDate format(YYYY-MM-DD):\n')
            year, month, day = map(int, date.split('-'))
            date1 = str(datetime.date(year, month, day))
            log(f'Start date selected is: {date1}', f'Logged {date1} date')
            
            date = input('Enter an endDate format(YYYY-MM-DD):\n')
            year, month, day = map(int, date.split('-'))
            date2 = str(datetime.date(year, month, day))
            log(f'Start date selected is: {date1}', f'Logged {date2} date')
            
            # URL CALL
            url = f'https://lb.mp.playtech.com/3rdparty/metrics/d_logins?startDate={date1}&endDate={date2}'
            logging.info(url)
            log(f'Called on {url}', f'{url} called')
    
            get_request = requests.get(url)
            response = get_request.content
            json_response = json.loads(response)

            # LOOPING THROUGH RESPONSE AND GETTING DATA INFORMATION
            for x in json_response['data']:
                # print(f'{x}') # PRINT TO GET WHOLE OBJECT ON CLI
                company = x['company']
                value = x['value']
                print(f'The company {company} has logged in {value} times''\n')
            
            # GET TOTAL VALUES + ADD
            sum_of_values = sum([i['value'] for i in json_response['data']])
            print(f'The total logins for requested dates: {sum_of_values}')
            logging.info(f'The total logins for requested dates: {sum_of_values}')
            log(f'Total logins for Operation: {sum_of_values}', f'total logins: {sum_of_values}')
                            
            break
        except (TypeError, ValueError, NameError, UnboundLocalError): 
            print('This is the incorrect date string format. It should be YYYY-MM-DD\n')
            logging.error('Error: This is the incorrect date string format. It should be YYYY-MM-DD\n')
            log(f'Error on date format. Retry!', f'Incorrect format. Forced retry')
            continue
        finally:
            # CHECK IF CURRENT DIRECTORY EXISTS & CREATE IF NOT
            path = os.getcwd()
            new_folder = '/extracted-json-data'
            created_folder = path + new_folder
           
            if not os.path.exists(created_folder):
                os.makedirs(created_folder, mode=0o777, exist_ok=False)
                print('Folder has been created.')
                logging.info('Folder has been created.')
                log(f'{created_folder} has been created', '{created_folder} created!')
            else:
                print('Folder already exists.')
                logging.warning('Folder already exists.')
                log(f'{created_folder} already exists', f'{created_folder} already exists')
                
            # 2. If file exists display that file for dates
            
            my_created_file = f'{created_folder}/metrics_login_admin-DATA-{date1}-TO-{date2}.json'
                            
            if Path(f'{my_created_file}').is_file():
                print('File already exists.')
                logging.warning('File already exists.', 'Folder exists')
                log(f'{my_created_file} already exists', 'File already exists. Skipping!')
            else:
                with open(f'{my_created_file}', 'w+') as write_file:           
                    json.dump(json_response['data'], write_file, indent=4, sort_keys=True)
                print(f'File Saved in folder {created_folder}!')   
                logging.info(f'File Saved in folder {created_folder}!\n')
                log(f'{my_created_file} being saved in folder!', f'File {my_created_file} saved!')
            
            # TODO:             
            # 3. FIX ERROR ON BREAK/CONTINUE CLAUSE WHEN INCORRECT INPUT FORMAT     

if __name__ == '__main__': 
    try:
        main()
    except KeyboardInterrupt:
        print('\nClosiinnnggg!!!')
        logging.warning('\nClosiinnnggg!!!')