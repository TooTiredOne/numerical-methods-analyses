from View import *


class Controller:
    def __init__(self):

        #setting up main window
        self.root = tk.Tk()
        self.root.title("Graphics of Numerical and Exact solutions")
        self.root.geometry("{0}x{1}+0+0".format(
            self.root.winfo_screenwidth() - 5, self.root.winfo_screenheight() - 5))

        #initializing Model and View
        self.model = Model()
        self.view = View(self.root, self.model)

        #starting the application
        self.start()

        #addong functionality to buttons
        self.view.b_solve.bind("<Button-1>", self.solve_dif_eq)
        self.view.b_glob_er.bind("<Button-1>", self.calc_glob)

        self.root.mainloop()

    def start(self):
        """starting the application with default values of IVP"""
        self.model.solve_dif_eq(2, 1, 5, 20)
        self.model.compute_glob_er(2, 1, 5, 10, 20)
        self.view.plot_dif_eq()
        self.view.plot_loc_er()
        self.view.plot_glob_er()

    def solve_dif_eq(self, event):
        """solving differential equations
        and plotting charts of different methods"""

        if not self.read_dif_eq_input():
            return False

        self.model.solve_dif_eq(self.y0, self.x0, self.X, self.N)
        self.view.plot_dif_eq()
        self.view.plot_loc_er()

    def calc_glob(self, event):
        """calculating global errors of different methods"""

        if not self.read_glob_er_input():
            return False

        self.model.compute_glob_er(self.y0, self.x0, self.X, self.Ni, self.Nf)
        self.view.plot_glob_er()

    def read_dif_eq_input(self):
        """reading the input for differential equations"""
        self.y0 = self.view.e_y0.get()
        self.x0 = self.view.e_x0.get()
        self.X = self.view.e_X.get()
        self.N = self.view.e_N.get()

        valid = True

        if not self.is_number(self.view.e_y0.get()):
            self.view.e_y0.delete(0, 'end')
            self.view.e_y0.insert(0, "INPUT NUM")
            valid = False

        if not self.is_number(self.view.e_x0.get()):
            self.view.e_x0.delete(0, 'end')
            self.view.e_x0.insert(0, "INPUT NUM")
            valid = False

        if not self.is_number(self.view.e_X.get()):
            self.view.e_X.delete(0, 'end')
            self.view.e_X.insert(0, "INPUT NUM")
            valid = False

        if not self.is_int(self.view.e_N.get()):
            self.view.e_N.delete(0, 'end')
            self.view.e_N.insert(0, "INPUT NUM")
            valid = False

        if valid:
            self.y0 = float(self.view.e_y0.get())
            self.x0 = float(self.view.e_x0.get())
            self.X = float(self.view.e_X.get())
            self.N = int(self.view.e_N.get())

            if self.y0 * self.x0 == 1:
                valid = False
                self.view.e_y0.delete(0, 'end')
                self.view.e_x0.delete(0, 'end')
                self.view.e_y0.insert(0, 'INVALID')
                self.view.e_x0.insert(0, 'INVALID')

            if self.x0 == 0:
                valid = False
                self.view.e_x0.delete(0, 'end')
                self.view.e_x0.insert(0, "INVALID")

            if self.X == 0:
                self.view.e_X.delete(0, 'end')
                self.view.e_X.insert(0, "INVALID")
                valid = False

            if self.X <= self.x0:
                self.view.e_X.delete(0, 'end')
                self.view.e_X.insert(0, "INVALID")
                self.view.e_x0.delete(0, 'end')
                self.view.e_x0.insert(0, "INVALID")
                valid = False

        return valid

    def read_glob_er_input(self):
        """reading the input for global errors"""
        if not self.read_dif_eq_input():
            return False

        self.Ni = self.view.e_Ni.get()
        self.Nf = self.view.e_Nf.get()

        valid = True

        if not self.is_int(self.view.e_Ni.get()):
            self.view.e_Ni.delete(0, 'end')
            self.view.e_Ni.insert(0, "INPUT NUM")
            valid = False

        if not self.is_int(self.view.e_Nf.get()):
            self.view.e_Nf.delete(0, 'end')
            self.view.e_Nf.insert(0, "INPUT NUM")
            valid = False

        if valid:
            self.Ni = int(self.view.e_Ni.get())
            self.Nf = int(self.view.e_Nf.get())

        return valid

    def is_int(self, s):
        """checking if s is int"""
        try:
            int(s)
            return True
        except ValueError:
            return False

    def is_number(self, s):
        """checking if s is number"""
        try:
            float(s)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    controller = Controller()
