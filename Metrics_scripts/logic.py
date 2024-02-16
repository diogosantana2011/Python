import logging , logging.handlers , datetime , os , json , requests , config
from pathlib import Path
from utils import db_trace, checkIsDir

def mainLogicApi(userType):
    # LOGGING
    fmtstr = '%(asctime)s: %(levelname)s: %(funcName)s: Line: %(lineno)d %(message)s' 
    datestr = '%d/%m/%Y %I:%M:%S %p'
    logging.basicConfig(
        level=logging.DEBUG,
        filename=config.logs_filename, 
        filemode='w+',
        format=fmtstr,
        datefmt=datestr
    )

    checkIsDir()
    try:            
        # DATE INPUTS
        date = input('Enter an startDate format(YYYY-MM-DD):\n')
        year, month, day = map(int, date.split('-'))
        date1 = str(datetime.date(year, month, day))
        db_trace(f'Start date selected is: {date1}', f'Logged {date1} date')
        
        date = input('Enter an endDate format(YYYY-MM-DD):\n')
        year, month, day = map(int, date.split('-'))
        date2 = str(datetime.date(year, month, day))
        db_trace(f'Start date selected is: {date1}', f'Logged {date2} date')
        
        if userType == 'ADMIN':
            # URL CALL
            url = f'{config.metrics_api}/i_logins?startDate={date1}&endDate={date2}'
            logging.info(url)
            db_trace(f'Called on {url}', f'{url} called')
        elif userType == 'MKT':
            # URL CALL
            url = f'{config.metrics_api}/l_logins?startDate={date1}&endDate={date2}'
            logging.info(url)
            db_trace(f'Called on {url}', f'{url} called')
        elif userType == 'WH':
            # URL CALL
            url = f'{config.metrics_api}/d_logins?startDate={date1}&endDate={date2}'
            logging.info(url)
            db_trace(f'Called on {url}', f'{url} called')

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
        db_trace(f'Total logins for Operation: {sum_of_values}', f'total logins: {sum_of_values}')
    except:
        print('This is the incorrect date string format. It should be YYYY-MM-DD\n')
        logging.error('Error: This is the incorrect date string format. It should be YYYY-MM-DD\n')
        db_trace(f'Error on date format. Retry!', f'Incorrect format. Forced retry')
    finally:
            # CHECK IF CURRENT DIRECTORY EXISTS & CREATE IF NOT
            path = os.getcwd()
            new_folder = '/extracted-json-data'
            created_folder = path + new_folder
           
            if not os.path.exists(created_folder):
                os.makedirs(created_folder, mode=0o777, exist_ok=False)
                print('Folder has been created.')
                logging.info('Folder has been created.')
                db_trace(f'{created_folder} has been created', f'{created_folder} created!')
            else:
                print('Folder already exists.')
                logging.warning('Folder already exists.')
                db_trace(f'{created_folder} already exists', f'{created_folder} already exists')
                
            # 2. If file exists display that file for dates
            
            my_created_file = f'{created_folder}/metrics_login-DATA-{date1}-TO-{date2}.json'
                            
            if Path(f'{my_created_file}').is_file():
                print('File already exists.')
                logging.warning('File already exists.')
                db_trace(f'{my_created_file} already exists', 'File already exists. Skipping!')
            else:
                with open(f'{my_created_file}', 'w+') as write_file:           
                    json.dump(json_response['data'], write_file, indent=4, sort_keys=True)
                print(f'File Saved in folder {created_folder}!')   
                logging.info(f'File Saved in folder {created_folder}!\n')
                db_trace(f'{my_created_file} being saved in folder!', f'File {my_created_file} saved!')  