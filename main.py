import os
import ctypes

from typing import Any, Callable

from time import sleep
from keyboard import send, write
from Controller.lib.WindowHandler import State
from Controller.lib.WindowHandler.managers import (
    event_windowCreated,
    searchForWindowByTitle,
    doesWindowExistIsItForeground,
)

from threading import Thread


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
            print(f"[ {number + 1} ]: {labelTuple[0]} ")

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


class Parser:
    def __init__(self, filePath, commentDelim: str = "#") -> None:
        self.commentDelim = commentDelim
        self.origLines = None
        self.comments = []
        self.words = []
        self.collapsedList = []

        with open(filePath) as f:
            self.origLines = f.readlines()

        for line in self.origLines:
            match line[0]:
                case "[":
                    pass
                case self.commentDelim:
                    self.comments.append(line)
                    pass
                case _:
                    self.words.append(line)
                    pass

    def breakDownAllStrings(self, delim: str = " "):
        self.collapsedList = []

        for word in self.words:
            if delim in word:
                for sub in word.split(delim):
                    self.collapsedList.append(sub)

                continue

            self.collapsedList.append(word)

        return self.collapsedList


def loadConfigFiles():

    configFiles = []
    for dirpath, _, filenames in os.walk("."):
        for file in filenames:
            if file.startswith("default_"):
                return [f"{dirpath}/{file}", True]

            elif file.startswith("list_"):
                configFiles.append(f"{dirpath}/{file}")

    return configFiles


def wordHandlerProc(wordList: list[str]):
    wordList = [word.replace("\n", "") for word in wordList]

    actionWaitTime = 0.3

    haveWindow = searchForWindowByTitle(".docx")
    if haveWindow == None:
        raise Exception("Could not find document with '.docx' file extension")

    haveWindow.tryActivate()

    haveWindow = doesWindowExistIsItForeground(haveWindow.windowTitle)
    if not haveWindow[0] or not haveWindow[1]:
        raise Exception("Failed to raise Word Window")

    send("ctrl+h")
    win = State()
    thread = event_windowCreated(
        lambda w: win.setVal(w), {"keyword": "Find and Replace"}
    )
    thread.join()
    sleep(0.5)

    for word in wordList:
        write(word.lower())
        sleep(actionWaitTime)

        send("tab")
        sleep(actionWaitTime)

        if " " in word:
            write(" ".join([subWord.capitalize() for subWord in word.split(" ")]))
        else:
            write(word.capitalize())

        sleep(actionWaitTime)

        send("alt+a")
        sleep(actionWaitTime)

        doneWin = State()
        thread = event_windowCreated(
            lambda w: doneWin.setVal(w), {"keyword": "Microsoft Word", "exact": True}
        )
        thread.join()

        doneWin.val.tryDestroy()
        sleep(1)
        didDestroy = doesWindowExistIsItForeground(doneWin.val.windowTitle)

        if didDestroy[0] != False and didDestroy[1] != False:
            raise Exception("Failed to close Confirmation Window")


def main():
    configs = loadConfigFiles()
    if len(configs) == 2 and configs[1] == True:
        choice = 0
    else:
        men = Menu([[config, None] for config in configs])
        choice = men.show(False)[0]

    wordHandlerProc(Parser(configs[choice]).words)


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    def points(self):
        return self.__getattribute__("x"), self.__getattribute__("y")

    def __repr__(self) -> str:
        return str(f"x: {self.__getattribute__('x')}, y: {self.__getattribute__('y')}")


def cursorCheck():
    def getCursorPos():
        out = Point()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(out))

        return out.points()

    x, y = getCursorPos()

    while 10 <= x or 10 <= y:
        sleep(0.2)
        x, y = getCursorPos()

    print("\n\n!!! EMERGENCY STOP !!!\n\n")
    os._exit(1)


stopCheck = Thread(target=cursorCheck, daemon=True)
stopCheck.start()
main()
