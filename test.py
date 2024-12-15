class Parent:
    def greet(self):
        return "Hello from Parent!"

class Child(Parent):
    x = super().greet()
    def greet(self):
        parent_message = '-'
        return parent_message + " And hello from Child!"

obj = Child()
print(obj.greet())
