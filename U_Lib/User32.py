import ctypes
from .Point import Point


class User32:

    @staticmethod
    def __user32__(functionName: str, args: tuple | object):
        if type(args) != tuple:
            args = (args,)

        ctypes.windll.user32[functionName](*[ctypes.byref(arg) for arg in args])

    @staticmethod
    def GetCursorPos():
        out = Point()
        User32.__user32__("GetCursorPos", out)

        return out.points()
