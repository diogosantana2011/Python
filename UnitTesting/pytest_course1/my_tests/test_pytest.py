import pytest

@pytest.fixture(scope="session", autouse=True)
def setupSession():
    print('\n Setup session!')

@pytest.fixture(scope="session", autouse=True)
def setupModule():
    print('\n Setup module!')

@pytest.fixture(scope="session", autouse=True)
def setupFunction():
    print('\n Setup function!')

def test1():
    print('\n Executing test1!')
    assert True

def test2():
    print('\n Executing test 2!')
    assert True