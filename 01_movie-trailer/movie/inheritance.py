
class Parent():

    def __init__(self, last_name, eye_color):
        print("Parent constructor called")
        self.last_name = last_name
        self.eye_color = eye_color

    def show_info(self):
        print("Last name: ", self.last_name)
        print("Eye color: ", self.eye_color)


class Child(Parent):
    def __init__(self, last_name, eye_color, number_of_toys):
        print("Child constructor called")
        Parent.__init__(self, last_name, eye_color)
        self.number_of_toys = number_of_toys

    def show_info(self):
        print(self.last_name, self.eye_color, str(self.number_of_toys))


billy = Parent("Cyrus", "brown")
# print(billy.last_name)
billy.show_info()

miley = Child("Cyrus", "blue", 50)
# print(miley.last_name)
miley.show_info()