def setup_module(module):
    print("\n Setup Module!")

def teardown_module(module):
    print("\n Tearing down module!")

def setup_function(function):
    if function == test1:
        print("\n Setting up test 1!")
    elif function == test2:
        print("\n Setting up test 2!")
    else:
        print("\n Setting up unknown test!")

def teardown_function(function):
    if function == test1:
        print("\n Tearing down test 1!")
    elif function == test2:
        print("\n Tearing down test 2!")
    else:
        print("\n Tearing down unknown test!")

def test1():
    print('\nExecuting test1!')
    assert True

def test2():
    print('\nExecuting test2!')
    assert True