class A:
    x = 0
    def __init__(self, *args, **kwargs):
        self.x = kwargs['x']
    def getX(self) :
        print(self.x)
    
y = A(x = 20)
y.getX()

