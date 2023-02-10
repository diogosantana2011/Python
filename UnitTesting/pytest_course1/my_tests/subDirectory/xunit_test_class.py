class TestClass:
    @classmethod
    def setup_class(cls):
        print("\n Setup TestClass!")

    @classmethod
    def teardown_class(cls):
        print("\n Teardown TestClass!")

    def setup_method(self, method):
        if method == self.test1:
            print("\n Setting up test 1!")
        elif method == self.test2:
            print("\n Setting up test 2!")
        else:
            print("\n Setting up unknown test!")

    def teardown_method(self, method):
        if method == self.test1:
            print("\n Tearing down test 1!")
        elif method == self.test2:
            print("\n Tearing down test 2!")
        else:
            print("\n Tearing down unknown test!")

    def test1(self):
        print('\nExecuting test1!')
        assert True

    def test2(self):
        print('\nExecuting test2!')
        assert True