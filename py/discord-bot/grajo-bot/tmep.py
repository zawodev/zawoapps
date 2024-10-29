C = {
    "a": 1,
    "b": 2
}

for key in C.items():
    print(key)

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement this abstract method")

class Dog(Animal):

    # init using super and add breed
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        return self.name + " says Woof!"

