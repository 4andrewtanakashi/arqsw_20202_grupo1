import abc

class Meal(metaclass=abc.ABCMeta):
    # template method
    def do_meal(self):
        self.prepare_ingredients()
        self.cook()
        self.eat()
        self.clean_up()

    def eat(self):
        print("Mmm, that's good")

    @abc.abstractmethod
    def prepare_ingredients(self):
        pass

    @abc.abstractmethod
    def cook(self):
        pass

    @abc.abstractmethod
    def clean_up(self):
        pass 
