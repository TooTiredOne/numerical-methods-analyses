from Solution import *


class Model:
    def __init__(self):
        self.eu_errs = []
        self.rk_errs = []
        self.ieu_errs = []
        self.Ni = 0
        self.Nf = 0

    def solve_dif_eq(self, y0, x0, X, N):
        """solves differential equation for give initial values"""
        sol_func = MySolutionFunction()
        func = MyFunction()
        grid = Grid(y0, x0, X, N)

        # acquiring exact solution
        self.ex = ExactSolution(func, sol_func, grid)
        self.ex.solve()
        print(sol_func.c)

        # acquiring approximation by Euler's method and computing local errors
        self.eu = Euler_Method(func, grid, self.ex)
        self.eu.solve()
        self.eu.compute_local_errors()

        # acquiring approximation by Improved Euler's method and computing local errors
        self.ieu = Improved_Euler_Method(func, grid, self.ex)
        self.ieu.solve()
        self.ieu.compute_local_errors()

        # acquiring approximation by Runge Kutta's method and computing local errors
        self.rk = Runge_Kutta_Method(func, grid, self.ex)
        self.rk.solve()
        self.rk.compute_local_errors()

    def compute_glob_er(self, y0, x0, X, Ni, Nf):
        """computing global errors for given IVP and range of N"""
        self.Ni = Ni
        self.Nf = Nf

        self.eu_errs = []
        self.rk_errs = []
        self.ieu_errs = []

        for n in range(Ni, Nf + 1):
            grid_glob = Grid(y0, x0, X, n) # creating a grid with given N
            sol_func_glob = MySolutionFunction()
            func_glob = MyFunction()

            # acquiring exact solution
            ex_glob = ExactSolution(func_glob, sol_func_glob, grid_glob)
            ex_glob.solve()

            # acquiring approximation by Euler's method and computing global error at the last point
            eu_glob = Euler_Method(func_glob, grid_glob, ex_glob)
            eu_glob.solve()
            self.eu_errs.append(eu_glob.compute_global_error())

            # acquiring approximation by Improved Euler's method and computing global error at the last point
            ieu_glob = Improved_Euler_Method(func_glob, grid_glob, ex_glob)
            ieu_glob.solve()
            self.ieu_errs.append(ieu_glob.compute_global_error())

            # acquiring approximation by Runge Kutta's method and computing global error at the last point
            rk_glob = Runge_Kutta_Method(func_glob, grid_glob, ex_glob)
            rk_glob.solve()
            self.rk_errs.append(rk_glob.compute_global_error())
