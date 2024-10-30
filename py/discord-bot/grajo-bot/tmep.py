C = {
    "a": 1,
    "b": 2
}

B = {"b": 3}

C.update(B)
print(C)

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

