class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def custom_dict(self):
        result = self.__dict__
        result['1'] = 32

        return result

# Создаем несколько экземпляров класса
obj1 = MyClass("John", 25)
obj2 = MyClass("Alice", 30)


print(obj1.custom_dict())