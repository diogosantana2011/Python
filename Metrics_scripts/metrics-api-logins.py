#
# Metrics API data
# Get login values for specified user and add them = result
# Then extract them to file as JSON
#

import logic

def main(): 
    user_choice = input('Which user would you like to query? (ADMN, MKT or WH)\n Please enter exactly ADMIN, MKT ... \n')
    logic.mainLogicApi(user_choice)
    
if __name__ == '__main__': 
    main()