import tkinter as tk
from Model import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class View:
    def __init__(self, root, model: Model):
        self.root = root
        self.model = model
        self.f_left = tk.Frame(root)
        self.f_mid = tk.Frame(root)
        self.f_right = tk.Frame(root)
        self.f_right_up = tk.Frame(self.f_right)
        self.f_right_down = tk.Frame(self.f_right)

        self.f_y0 = tk.Frame(self.f_mid)
        self.l_y0 = tk.Label(self.f_y0, text="y0")
        self.e_y0 = tk.Entry(self.f_y0, width=10, justify='center')

        self.f_x0 = tk.Frame(self.f_mid)
        self.l_x0 = tk.Label(self.f_x0, text="x0")
        self.e_x0 = tk.Entry(self.f_x0, width=10, justify='center')

        self.f_X = tk.Frame(self.f_mid)
        self.l_X = tk.Label(self.f_X, text="X  ")
        self.e_X = tk.Entry(self.f_X, width=10, justify='center')

        self.f_N = tk.Frame(self.f_mid)
        self.l_N = tk.Label(self.f_N, text="N ")
        self.e_N = tk.Entry(self.f_N, width=10, justify='center')

        self.f_solve = tk.Frame(self.f_mid)
        self.b_solve = tk.Button(self.f_solve, text='Solve\n Dif. Equation')

        self.f_Ni = tk.Frame(self.f_mid)
        self.l_Ni = tk.Label(self.f_Ni, text="Ni ")
        self.e_Ni = tk.Entry(self.f_Ni, width=10, justify='center')

        self.f_Nf = tk.Frame(self.f_mid)
        self.l_Nf = tk.Label(self.f_Nf, text="Nf ")
        self.e_Nf = tk.Entry(self.f_Nf, width=10, justify='center')

        self.f_glob_er = tk.Frame(self.f_mid)
        self.b_glob_er = tk.Button(self.f_glob_er, text='Calculte\nGlobal Errors')

        self.e_y0.insert(0, "2")
        self.e_x0.insert(0, "1")
        self.e_X.insert(0, "5")
        self.e_N.insert(0, "100")

        self.e_Ni.insert(0, "10")
        self.e_Nf.insert(0, "20")

        self.display_widgets()

    def display_widgets(self):
        """placing elements of GUI in main window"""
        self.f_left.pack(side=tk.LEFT, padx=20)
        self.f_mid.pack(side=tk.LEFT)
        self.f_right.pack(side=tk.LEFT, padx=10)
        self.f_right_up.pack(side=tk.TOP)
        self.f_right_down.pack(side=tk.TOP)

        self.f_y0.pack(side=tk.TOP)
        self.l_y0.pack(side=tk.LEFT)
        self.e_y0.pack(side=tk.LEFT, padx=10)

        self.f_x0.pack(side=tk.TOP)
        self.l_x0.pack(side=tk.LEFT)
        self.e_x0.pack(side=tk.LEFT, padx=10)

        self.f_X.pack(side=tk.TOP)
        self.l_X.pack(side=tk.LEFT)
        self.e_X.pack(side=tk.LEFT, padx=10)

        self.f_N.pack(side=tk.TOP)
        self.l_N.pack(side=tk.LEFT)
        self.e_N.pack(side=tk.LEFT, padx=10)

        self.f_solve.pack(side=tk.TOP, pady=20)
        self.b_solve.pack(side=tk.TOP, fill=tk.BOTH, pady=5)

        self.f_Ni.pack(side=tk.TOP)
        self.l_Ni.pack(side=tk.LEFT)
        self.e_Ni.pack(side=tk.LEFT, padx=10)

        self.f_Nf.pack(side=tk.TOP)
        self.l_Nf.pack(side=tk.LEFT)
        self.e_Nf.pack(side=tk.LEFT, padx=9)

        self.f_glob_er.pack(side=tk.TOP, pady=20)
        self.b_glob_er.pack(side=tk.TOP, fill=tk.BOTH, pady=5)

    def plot_dif_eq(self):
        """plotting charts of different methods"""
        try:
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.pack_forget()
        except AttributeError:
            pass

        f = Figure(figsize=(8, 8), dpi=100)
        p = f.add_subplot(111)

        p.plot(self.model.ex.x_coord_plot, self.model.ex.y_coord_plot, c = 'C6')
        p.scatter(self.model.ex.x_coord, self.model.ex.y_coord, c = 'C6')
        p.plot(self.model.eu.x_coord, self.model.eu.y_coord, marker='o')
        p.plot(self.model.ieu.x_coord, self.model.ieu.y_coord, marker='o')
        p.plot(self.model.rk.x_coord, self.model.rk.y_coord, marker='o')

        p.set_ylabel('y')
        p.set_xlabel('x')

        p.legend(['Exact', 'EU', "IEU", "RK"])
        p.set_title("Solutions")
        if max(self.model.ex.y_coord_plot) >= 1e5 or max(self.model.eu.y_coord) >= 1e5 \
                or max(self.model.ieu.y_coord) >= 1e5 or max(self.model.rk.y_coord) >= 1e5:
            p.set_ylim([-100, 100])

        if min(self.model.ex.y_coord_plot) <= -1e5 or min(self.model.eu.y_coord) <= -1e5 \
                or min(self.model.ieu.y_coord) <= -1e5 or min(self.model.rk.y_coord) <= -1e5:
            p.set_ylim([-100, 100])

        self.canvas = FigureCanvasTkAgg(f, self.f_left)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.f_left)
        self.toolbar.update()

        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def plot_glob_er(self):
        """plotting total approximation errors of different methods"""
        try:
            self.canvas_glob.get_tk_widget().pack_forget()
            self.toolbar_glob.pack_forget()

        except AttributeError:
            pass

        f = Figure(figsize=(6, 4), dpi=100)
        p = f.add_subplot(111)

        p.plot(range(self.model.Ni, self.model.Nf + 1), self.model.eu_errs, marker='o')
        p.plot(range(self.model.Ni, self.model.Nf + 1), self.model.ieu_errs, marker='o')
        p.plot(range(self.model.Ni, self.model.Nf + 1), self.model.rk_errs, marker='o')

        p.legend(['EU', "IEU", 'RK'])
        p.set_title("Total approximation error")
        p.set_xlabel("N")
        p.set_ylabel("Error")
        self.canvas_glob = FigureCanvasTkAgg(f, self.f_right_down)
        self.canvas_glob.draw()
        self.canvas_glob.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.toolbar_glob = NavigationToolbar2Tk(self.canvas_glob, self.f_right_down)
        self.toolbar_glob.update()

        self.canvas_glob._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def plot_loc_er(self):
        """plotting local errors of different methods"""
        try:
            self.canvas_loc.get_tk_widget().pack_forget()
            self.toolbar_loc.pack_forget()
        except AttributeError:
            pass

        f = Figure(figsize=(6, 4), dpi=100)
        p = f.add_subplot(111)

        p.plot(self.model.eu.x_coord, self.model.eu.local_error, marker='o')
        p.plot(self.model.ieu.x_coord, self.model.ieu.local_error, marker='o')
        p.plot(self.model.rk.x_coord, self.model.rk.local_error, marker='o')

        p.set_xlabel('x')
        p.set_ylabel('Local Error')

        if max(self.model.eu.local_error) >= 1e5 or max(self.model.ieu.local_error) >= 1e5 \
                or max(self.model.rk.local_error) >= 1e5:
            p.set_ylim([-100, 100])

        if min(self.model.eu.local_error) <= -1e5 or min(self.model.ieu.local_error) <= -1e5 \
                or min(self.model.rk.local_error) <= -1e5:
            p.set_ylim([-100, 100])

        p.legend(['EU', "IEU", 'RK'])
        p.set_title("Local Errors")
        self.canvas_loc = FigureCanvasTkAgg(f, self.f_right_up)
        self.canvas_loc.draw()
        self.canvas_loc.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.toolbar_loc = NavigationToolbar2Tk(self.canvas_loc, self.f_right_up)
        self.toolbar_loc.update()

        self.canvas_loc._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
