class TestClass:
    def __init__(self):
        self.b = 2
    def checkattri(self):
        if hasattr(self, 'a'):
            print("has a")
        if hasattr(self, 'b'):
            print("has b")
    def deletea(self):
        del self.b
        if hasattr(self, 'b'):
            print("has b")


if __name__ == '__main__':
    testclass = TestClass()
    testclass.checkattri()
    testclass.deletea()
    testclass.checkattri()
