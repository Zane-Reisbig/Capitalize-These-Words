import os

from time import sleep
from keyboard import send, write

from U_Lib.Menu import Menu
from U_Lib.Parser import Parser

from U_Lib.User32 import User32

from Controller.lib.WindowHandler import State, Window
from Controller.lib.WindowHandler.managers import (
    event_windowCreated,
    searchForWindowByTitle,
    doesWindowExistIsItForeground,
)

from threading import Thread, Event


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
    wordReference = State()
    thread = event_windowCreated(
        lambda w: wordReference.setVal(w), {"keyword": "Find and Replace"}
    )
    thread.join()
    wordReference: Window = wordReference.val
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
        doneWin: Window = doneWin.val

        doneWin.tryDestroy()
        sleep(1)
        didDestroy = doesWindowExistIsItForeground(doneWin.windowTitle)

        if didDestroy[0] != False and didDestroy[1] != False:
            raise Exception("Failed to close Confirmation Window")

    wordReference.tryDestroy()


def main():
    configs = loadConfigFiles()
    if len(configs) == 2 and configs[1] == True:
        choice = 0
    else:
        men = Menu([[config, None] for config in configs])
        choice = men.show(False)[0]

    wordHandlerProc(Parser(configs[choice]).words)


def cursorCheck(event: Event):
    x, y = User32.GetCursorPos()

    while not event.is_set():
        x, y = User32.GetCursorPos()

        if x < 10 or y < 10:
            print("\n\n!!! EMERGENCY STOP !!!\n\n")
            os._exit(1)

        sleep(0.2)


stopThreadEvent = Event()
watcher = Thread(target=cursorCheck, daemon=True, args=(stopThreadEvent,))
watcher.start()

error = None
try:
    main()
except Exception as e:
    error = e
    stopThreadEvent.set()
finally:
    print("Watcher Thread Stopped...")
    watcher.join()
    sleep(0.4)
    raise error
