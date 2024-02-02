#
# Admin Metrics API data
# Get login values for all and add them = result
#

import logic

# Alert Colors
# TODO: Confirm how to stop color after script completion
# red = "\x1B[31m"    # to highlight messages
# green = '\x1b[32m'

def main(): 
    logic.mainLogicApi('ADMIN')
    
if __name__ == '__main__': 
    main()