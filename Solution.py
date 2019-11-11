from Function import *
from Grid import *


class Solution(ABC):
    """An abstract class representing different solution methods (e.g. Exact, Numerical)
        for a given function y'=f(x,y) and grid"""

    def __init__(self, function: Function, grid: Grid):
        self.func = function
        self.grid = grid

        self.x_coord = []
        i = grid.x0
        for c in range(grid.N + 1):
            self.x_coord.append(i)
            i += grid.h

        self.y_coord = []

    @abstractmethod
    def solve(self):
        """solves y'=f(x,y) in a given grid"""
        pass


class ExactSolution(Solution):
    """A class representing Exact Solutions
        of a given function y'=f(x,y) for a given grid """

    def __init__(self, function: Function, sol_function: MySolutionFunction, grid: Grid):
        super().__init__(function, grid)
        self.sol_function = sol_function

        self.x_coord_plot = []
        i = grid.x0
        for c in range(grid.N * 100 + 1):
            self.x_coord_plot.append(i)
            i += grid.h/100

        self.y_coord_plot = []

    def solve(self):
        self.sol_function.compute_const(self.grid.x0, self.grid.y0)
        self.y_coord = [self.sol_function.compute(x) for x in self.x_coord]
        self.y_coord_plot = [self.sol_function.compute(x) for x in self.x_coord_plot]


class NumericalMethod(Solution):
    """An abstract class representing Numerical Solutions (e.g Euler, Improved Euler, Runge-Kutta)
            for a given function y'=f(x,y) and grid """

    def __init__(self, func: Function, grid: Grid, exact_sol: ExactSolution):
        super().__init__(func, grid)
        self.exact_sol = exact_sol
        self.local_error = []

    @abstractmethod
    def compute_global_error(self):
        """computes global error at the last point"""
        pass

    @abstractmethod
    def compute_local_errors(self):
        """computes local errors in all points"""
        pass


class Euler_Method(NumericalMethod):

    def compute_global_error(self):
        return self.exact_sol.y_coord[len(self.x_coord) - 1] - self.y_coord[len(self.x_coord) - 1]

    def compute_local_errors(self):
        self.local_error = [0]
        for i in range(1, len(self.x_coord)):
            self.local_error.append(self.exact_sol.y_coord[i] - self.exact_sol.y_coord[i - 1] \
                                    - self.grid.h * self.func.compute(self.x_coord[i], self.exact_sol.y_coord[i]))

    def compute_y(self, i):
        """computes i-th y by Euler's method using (i-1)-th y and x"""
        if i == 0:
            return self.grid.y0
        else:
            return self.y_coord[i - 1] + self.grid.h * self.func.compute(self.x_coord[i - 1],
                                                                         self.y_coord[i - 1])

    def solve(self):
        for i in range(len(self.x_coord)):
            self.y_coord.append(self.compute_y(i))


class Improved_Euler_Method(NumericalMethod):

    def compute_global_error(self):
        return self.exact_sol.y_coord[len(self.x_coord) - 1] - self.y_coord[len(self.x_coord) - 1]

    def compute_local_errors(self):
        self.local_error = [0]
        for i in range(1, len(self.x_coord)):
            k1 = self.func.compute(self.x_coord[i - 1], self.exact_sol.y_coord[i - 1])
            k2 = self.func.compute(self.x_coord[i - 1] + self.grid.h,
                                   self.exact_sol.y_coord[i - 1] + self.grid.h * k1)
            self.local_error.append(self.exact_sol.y_coord[i] \
                                    - (self.exact_sol.y_coord[i - 1] + (k1 + k2) * self.grid.h / 2))

    def compute_y(self, i):
        """computes i-th y by Improved Euler's method using (i-1)-th y and x"""
        if i == 0:
            return self.grid.y0
        else:
            k1 = self.func.compute(self.x_coord[i - 1], self.y_coord[i - 1])
            k2 = self.func.compute(self.x_coord[i - 1] + self.grid.h,
                                   self.y_coord[i - 1] + self.grid.h * k1)
            return self.y_coord[i - 1] + (k1 + k2) * self.grid.h / 2

    def solve(self):
        for i in range(len(self.x_coord)):
            self.y_coord.append(self.compute_y(i))


class Runge_Kutta_Method(NumericalMethod):

    def compute_global_error(self):
        return self.exact_sol.y_coord[len(self.x_coord) - 1] - self.y_coord[len(self.x_coord) - 1]

    def compute_local_errors(self):
        self.local_error = [0]
        for i in range(1, len(self.x_coord)):
            k1 = self.func.compute(self.x_coord[i - 1], self.y_coord[i - 1])
            k2 = self.func.compute(self.x_coord[i - 1] + self.grid.h / 2,
                                   self.y_coord[i - 1] + self.grid.h * k1 / 2)
            k3 = self.func.compute(self.x_coord[i - 1] + self.grid.h / 2,
                                   self.y_coord[i - 1] + self.grid.h * k2 / 2)
            k4 = self.func.compute(self.x_coord[i - 1] + self.grid.h,
                                   self.y_coord[i - 1] + self.grid.h * k3)
            self.local_error.append(self.exact_sol.y_coord[i] -
                                    (self.y_coord[i - 1] + self.grid.h * (k1 + 2 * k2 + 2 * k3 + k4) / 6))

    def compute_y(self, i):
        """computes i-th y by Runge-Kutta’s method using (i-1)-th y and x"""
        if i == 0:
            return self.grid.y0
        else:
            k1 = self.func.compute(self.x_coord[i - 1], self.y_coord[i - 1])
            k2 = self.func.compute(self.x_coord[i - 1] + self.grid.h / 2,
                                   self.y_coord[i - 1] + self.grid.h * k1 / 2)
            k3 = self.func.compute(self.x_coord[i - 1] + self.grid.h / 2,
                                   self.y_coord[i - 1] + self.grid.h * k2 / 2)
            k4 = self.func.compute(self.x_coord[i - 1] + self.grid.h,
                                   self.y_coord[i - 1] + self.grid.h * k3)
            return self.y_coord[i - 1] + self.grid.h * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def solve(self):
        for i in range(len(self.x_coord)):
            self.y_coord.append(self.compute_y(i))

