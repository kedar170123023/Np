class A_from:
    x = 2

y = {
    "ram" : 2
}
# get class name from string
a = eval("A"+"_from")

print(a.x )
#prints 2

class Person:
    name = 'Adam'
    
p = Person()
print('Before modification:', p.name)

# setting name to 'John'
setattr(p, 'name', 'John')

print('After modification:', p.name)

# hasattr
# getattr

x = 5
print(callable(x))

def testFunction():
  print("Test")

y = testFunction
print(callable(y)) #returns true

class Foo:
  def __call__(self):
    print('Print Something')

print(callable(Foo)) #makes it callable

class Foo:
  def __call__(self):
    print('Print Something')

InstanceOfFoo = Foo()

# Prints 'Print Something'
InstanceOfFoo()

vars()
globals() #returns a dictionary containing variables
locals()


globals() #dictionary returning all global variables
locals()  # dictionary returning all local variables

