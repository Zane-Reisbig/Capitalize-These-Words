import ctypes


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    x: int
    y: int

    def points(self):
        return self.x, self.y

    def __repr__(self) -> str:
        return str(f"Point(x={self.x}, y={self.y})")
