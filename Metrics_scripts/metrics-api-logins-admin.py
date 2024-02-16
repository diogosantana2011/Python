#
# Admin Metrics API data
# Get login values for all and add them = result
#

import logic

# Alert Colors
# TODO: Confirm how to stop color after script completion
# red = "\x1B[31m"    # to highlight messages
# green = '\x1b[32m'
# TODO: 
# ADD INPUT FOR TYPE OF USER
# FROM HERE CALL ON URL BASED ON THIS TYPE OF USER 
# HAVING 1 SCRIPT FOR ALL 3 CALLS

def main(): 
    logic.mainLogicApi('ADMIN')
    
if __name__ == '__main__': 
    main()