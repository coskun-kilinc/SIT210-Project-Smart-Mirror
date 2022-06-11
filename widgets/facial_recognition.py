from abc import ABC, abstractmethod
import random

'''
Abstract Identification Interface
'''
class AbstractIdentifier(ABC):

    @abstractmethod
    def get_identity(self) -> str:
        raise NotImplementedError

'''
Dummy facial recognition for testing
'''
class DummyFacialRecognition(AbstractIdentifier):

    def __init__(self, indetity: str) -> None:
        super().__init__()
        self.identity = indetity


    def get_identity(self) -> str:
        check = random.random()
        if check < 0.5:
            return "unknown"
        else:
            return self.identity 


'''
Abstract Greeting Interface
'''
class AbstractGreeting(ABC):

    @abstractmethod
    def greeting(self) -> str:
        raise NotImplemented

'''
Concrete greeting implementation
'''
class GeneralGreeting(AbstractGreeting):
    greetings = [
        "Welcome back, ",
        "Hello, ",
        "Good to see you, ",
        "Hello there, "]

    def greeting(self, identity: str) -> str:
        choice = random.randint(0, 3)
        greeting = self.greetings[choice] + identity
        return greeting



identifier = DummyFacialRecognition("Josh")
#greeter = GeneralGreeting(DummyFacialRecognition("Josh"))
#print(greeter.greeting())

