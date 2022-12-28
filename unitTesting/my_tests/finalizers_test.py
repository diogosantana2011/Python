import pytest

@pytest.fixture()
def setup1():
    print('\n Setup 1!')
    yield
    print('\n Teardown 1!')

@pytest.fixture()
def setup2(request):
    print('\n Setup 2!')

    def teardown_a():
        print('\n Teardown A!')

    def teardown_b():
        print('\n Teardown B!')

    request.addfinalizer(teardown_a)
    request.addfinalizer(teardown_b)

def test1(setup1):
    print('\n Executing test1 !')
    assert True

def test2(setup2):
    print('\n Executing test2 !')
    assert True