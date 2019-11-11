class Grid:
    """A class representing Grid"""

    def __init__(self, y0, x0, X, N):
        """"x0 and y0 are initial values of IVP
            x is in range (x0, X)
            N is the amount of grids cells between x0 and X"""
        self.x0 = x0  # ivp
        self.y0 = y0  # ivp
        self.N = N  # number of "cells"
        self.X = X  # final value of x
        self.h = (X - x0) / N  # grid step