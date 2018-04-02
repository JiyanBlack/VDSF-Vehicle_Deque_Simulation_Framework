class people:
    def __init__(self, name):
        self.name = name


class student(people):
    def __init__(self, name):
        super().__init__(name)

    def sayhi(self):
        print(self.name)


a = student("black")
a.sayhi()