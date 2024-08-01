import os

from typing import Callable, Any
from time import sleep


class Menu:

    def __init__(self, items: list[tuple[str, Callable]]) -> None:

        self.items = items

    def __tryInt__(self, _with: Any):
        try:
            return True, int(_with)
        except:
            return False, _with

    def __getChoice__(self) -> int:
        message = f"Choice [1..{len(self.items)}] - "
        choice = (None, None)
        rangeCheck = lambda: choice[1] > 0 and choice[1] <= len(self.items)

        while not choice[0] or not rangeCheck():
            choice = self.__tryInt__(input(message))

            if not choice[0] or not rangeCheck():
                print(
                    f"{repr(choice[1])} is not a number between 0 and {len(self.items)}"
                )
                sleep(1)
                os.system("cls")
                self.__printMenu__()

        return choice[1] - 1

    def __printMenu__(self):
        for number, labelTuple in enumerate(self.items):
            print(f"[ {number + 1} ]: {repr(labelTuple[0])} ")

    def show(self, invoke=True):
        os.system("cls")
        self.__printMenu__()
        index = self.__getChoice__()

        print(f"Chose file: {self.items[index]}")
        sleep(0.4)
        os.system("cls")

        if invoke:
            self.items[index][1]()

        return (index, self.items[index][1])
