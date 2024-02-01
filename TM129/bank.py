#!/usr/bin/python3

import threading, time, sys

"""
A simulation of a bank account, intended to demonstrate non-determinacy due 
to timing (a race condition).

Two threads run concurrently, one making many deposits, one making many 
withdrawals. 

Non-determinacy can arise if a context switch happens in a critical region 
where the account balance is updated. The critical regions can be protected 
with a mutex lock. Discrepancy in the balance is detected by comparison with 
cumulative total of deposits and withdrawals.

A busy-wait delay loop is used inside the critical region to increase the 
chance of a context switch occurring. (Calling sleep() (almost) always causes 
context switch so race condition is then inevitable; sleep() also seems to 
have limited precision). Print statements also use cpu cycles so change the 
likelihood of race condition occurring. However, redirecting output to file 
or pipe can change this substantially.

Future: possibly need separately controlled time delay in threads?

"""

# default values
delay = 0.01        # secs
count = 50          # transactions per thread
exit_on_error = False
quiet = False
locking = False
red = "\x1B[31m"    # to highlight messages
reset = "\x1B[0m"

def usage():
    ''' Print usage message '''
    print("Usage: ", sys.argv[0], "[options] [delay] [count]")
    print("Simulate non-determinacy (race condition) in concurrent debit and withdrawal transactions")
    print("  delay\t\ttime (secs) spent in transaction, default", delay)
    print("  count\t\tnumber of transactions, default", count)
    print("Options:")    
    print("  -q --quiet\tsuppress printing of each transaction")
    print("  -e --exit\texit after first transaction error")
    print("  -l --lock\tlock account during each transaction")
    print("  --help\tprint this message")


def parse_args():
    """ Parse command line arguments, print usage if invalid """
    global delay, count, exit_on_error, quiet, locking
    try:
        if "-e" in sys.argv:
            exit_on_error = True
            sys.argv.remove("-e")
        if "--exit" in sys.argv:
            exit_on_error = True
            sys.argv.remove("--exit")
        if "-q" in sys.argv:
            quiet = True
            sys.argv.remove("-q")
        if "--quiet" in sys.argv:
            quiet = True
            sys.argv.remove("--quiet")
        if "-l" in sys.argv:
            locking = True
            sys.argv.remove("-l")
        if "--lock" in sys.argv:
            locking = True
            sys.argv.remove("--lock")
        if "--help" in sys.argv or len(sys.argv) > 3:
            sys.exit(2)
        if len(sys.argv) > 2:
            count = int(sys.argv[2])
        if len(sys.argv) > 1:
            delay = float(sys.argv[1])
    except:
        usage()
        raise


def busy_wait(delay):
    """ Keep cpu busy without sleeping """
    now = time.perf_counter()    # high resolution clock, measuring seconds
    end = now + delay
    # enter busy wait during which preemptive context switch may occur
    while now < end:
        now = time.perf_counter()


#----------------------------------------------------------------------------
class Account:
    """ Class to simulate a bank account """
    def __init__(self):
        self.balance = 0
        self.total_deposited = 0
        self.total_withdrawn = 0
        self.num_transactions = 0
        self.num_errors_detected = 0
        self.mutex = threading.Lock()


    def check(self, last_trans):
        """ check for discrepancy after last transaction """
        if locking:
            self.mutex.acquire()
        discrepancy = self.balance - (self.total_deposited - self.total_withdrawn)
        if locking:
            self.mutex.release()

        if (discrepancy != 0):
            self.num_errors_detected += 1
            print (red, "*** error: after", self.num_transactions, "transactions,", \
                   "discrepancy:", discrepancy, \
                   "last:", last_trans, reset)
            if exit_on_error:
                sys.exit(3)
            else:
                # correct balance to suppress repeat detection
                self.balance = self.total_deposited - self.total_withdrawn
           

    def deposit(self, amount):
        """ deposit an amount """
        # start of critical region wrt balance
        if locking:
            self.mutex.acquire()
        old_bal = self.balance                  # read old balance
        self.total_deposited += amount          # keep running total as check
        self.num_transactions += 1
        busy_wait(delay)                        # ...during which context switch may occur
        self.balance = old_bal + amount         # write new balance
        if locking:
            self.mutex.release()
        # end of critical region wrt balance
        self.check("deposit")
           

    def withdraw(self, amount):
        """ withdraw an amount """
        # start of critical region wrt balance
        if locking:
            self.mutex.acquire()
        old_bal = self.balance                  # read old balance
        self.total_withdrawn += amount          # keep running total as check
        self.num_transactions += 1
        busy_wait(delay)                        # ...during which context switch may occur
        self.balance = old_bal - amount         # write new balance
        if locking:
            self.mutex.release()
        # end of critical region wrt balance
        self.check("withdraw")

    
#----------------------------------------------------------------------------
class DepositThread(threading.Thread) :
    """ Thread to simulate deposit activity """

    def __init__(self, name, account, amount, count, delay):
        """ initialise variables """
        threading.Thread.__init__(self, name=name)
        self.account = account
        self.amount = amount
        self.count = count
        self.delay = delay

    def run(self):
        """ Make many deposits """
        for i in range(self.count):
            if not quiet:
                print ("Depositing:  %8.2f balance: %8.2f" %
                       (self.amount, self.account.balance))
            self.account.deposit(self.amount)
        print (self.name, "finishing")
 

#----------------------------------------------------------------------------
class WithdrawThread(threading.Thread) :
    """ Thread to simulate withdrawals """
    
    def __init__(self, name, account, amount, count, delay):
        """ initialise variables """
        threading.Thread.__init__(self, name=name)
        self.account = account
        self.amount = amount
        self.count = count
        self.delay = delay

    def run(self):
        """ Make many withdrawals """
        for i in range(self.count):
            if not quiet:
                print ("Withdrawing:  %8.2f balance: %8.2f" %
                       (self.amount, self.account.balance))
            self.account.withdraw(self.amount)
        print (self.name, "finishing")
        

#----------------------------------------------------------------------------
# main program

# deal with command line arguments
parse_args();

# create account
my_acc = Account()
 
# create threads
dt = DepositThread("Depositing thread", my_acc, 1000, count, delay)
wt = WithdrawThread("Withdrawing thread", my_acc, 200, count, delay)

# start threads running
dt.start()
wt.start()

# wait for threads to terminate and rejoin main thread
dt.join()
wt.join()

print ("Simulation complete")
print ("Final balance:", my_acc.balance)
print ("Account transactions:", my_acc.num_transactions)
print ("Discrepancies detected:", my_acc.num_errors_detected)

