from abc import ABC, abstractmethod  # Abstract Base Classes
import numpy as np


class Function(ABC):
    """"An abstract class representing some f(x, y)"""

    @abstractmethod
    def compute(self, x, y):
        """if y is none then method computes y = g(x)
           otherwise, the method computes y' = f(x, y)"""
        pass


class MyFunction(Function):
    """10th variant y' = f(x,y) function"""

    def compute(self, x, y):
        """computes y'= f(x,y) of 10th variant"""
        if x == 0:
            return np.nan

        try:
            if abs((-(y ** 2) / 3) - (2 / (3 * (x ** 2)))) >= np.inf:
                return np.nan
        except OverflowError:
            return np.nan

        return (-(y ** 2) / 3) - (2 / (3 * (x ** 2)))


class MySolutionFunction(Function):
    """represents y = g(x), which is a solution of
       y' = f(x,y) of 10th variant"""

    def __init__(self):
        """"initialize constant with some random value"""
        self.c = np.random.randn(1)[0]

    def is_almost_equal(self, x, y, epsilon=1 * 10 ** (-4)):
        """Return True if two values are close in numeric"""
        return abs(x - y) <= epsilon

    def compute(self, x, y=None):
        """computes y = g(x)"""
        if x == 0:
            return np.nan
        if x < 0:
            t = abs(x)
            if self.is_almost_equal(t**(1/3), -self.c):
                return np.nan
        else:
            if self.is_almost_equal(x**(1/3), -self.c):
                return np.nan

        if x < 0:
            t = abs(x)
            return (-2 * (t ** (1 / 3)) + self.c) / (x * (-(t ** (1 / 3)) + self.c))

        return (2 * (x ** (1 / 3)) + self.c) / (x * ((x ** (1 / 3)) + self.c))

    def compute_const(self, x0, y0):
        """computes constant with given x0 and y0"""

        if x0 < 0:
            t = abs(x0)
            self.c = (-(t ** (1 / 3)) * (y0 * x0 - 2)) / (1 - y0 * x0)
        else:
            self.c = ((x0 ** (1 / 3)) * (y0 * x0 - 2)) / (1 - y0 * x0)

