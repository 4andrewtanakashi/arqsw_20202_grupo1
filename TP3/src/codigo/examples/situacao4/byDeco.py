# create a class
class byDeco:

   # constructor
    def __init__(self, value):
        self._value = value

    # getting the values
    @property
    def value(self):
        print('Getting value')
        return self._value

    # setting the values
    @value.setter
    def value(self, value):
        print('Setting value to ' + value)
        self._value = value

    # deleting the values
    @value.deleter
    def value(self):
        print('Deleting value')
        del self._value


# create an object of class
x = byDeco('happy Coding')
print(x.value)

x.value = 'Hey Coder!'

# deleting the value
del x.value
