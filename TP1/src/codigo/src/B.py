from A import Class_A

class Class_B:
    def __init__(self, first_param):
        self.first_param = first_param

    def first_method(self):
        first_var = Class_A.first_method

    def second_method(self):
        second_var = Class_A.second_method

    def third_method(self):
        third_var = Class_A.third_method

    def fourth_method(self):
        pass

def main():
    cb = Class_B(first_param = 1)
    fourth_var = cb.fourth_method()

if __name__ == "__main__":
    main()