from abc import ABC, abstractmethod

class Device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

class Printer(Device):
    def turn_on(self):
        print("Printer is now ON")

    def turn_off(self):
        print("Printer is now OFF")

class Scanner(Device):
    def turn_on(self):
        print("Scanner is now ON")

    def turn_off(self):
        print("Scanner is now OFF")


s = Scanner()

s.turn_on()