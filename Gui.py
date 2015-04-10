from Tkinter import *
import Potential as Pt
from Range import Range
import WaveFunction as Wf
import Potential
import FiniteDifference
import Visualize
import math

def display():
    master = Tk()
    def label(text):
        Label(master, text=text).pack(anchor=W)
    # Returns a function which takes no arguments and returns the value of the variable
    def int_var(low, high, default):
        var = IntVar()
        var.set(default)
        Spinbox(master, from_=low, to=high, textvariable=var).pack(anchor=W)
        return var.get

    # Takes in a list of (name, value) pairs and displays a gui radio list to select one of these values
    # Returns a function which takes no arguments and returns the selected value
    def radio(possible_vals):
        selection = IntVar()
        for i, (name, val) in enumerate(possible_vals):
            Radiobutton(master, text=name, variable=selection, value=i).pack()
        return lambda : possible_vals[selection.get()][1]
    # Takes in a dictionary of (name, function) pairs and displays a GUI drop down menu to select init function
    def drop_down(dict):
        selection = StringVar()
        keys = dict.keys()
        selection.set(keys[0])
        OptionMenu(master, selection, *keys).pack(anchor=W)
        return lambda : dict[selection.get()]

    barrier_fun = lambda x : Pt.barrier(float(get_barrier_width()),float(get_barrier_height()))(x)
    crystal_fun = lambda x : Pt.crystal(float(get_crystal_depth()),float(get_crystal_width()))(x)
    traveling_wave_fun = lambda x: Wf.traveling_wave(float(get_energy()))(x) 

    label("Algorithm:")
    get_algorithm = int_var(1,2,2)

    label("Width:")
    get_width = int_var(0, 10000000, 20)

    label("Width divisions:")
    get_space_divisions = int_var(10, 500, 200)

    label("Simulation time:")
    get_max_time = int_var(5, 150, 10)

    label("Time divisions:")
    get_time_divisions = int_var(10, 2000, 1000)

    label("Potentials:")
    optionDict = {'KP-Crystal': crystal_fun, 'Harmonic Oscillator': Pt.harmonic_oscillator(), 'Barrier': barrier_fun, 'Infinite Well': Pt.infinite_well()}
    get_selected_potential = drop_down(optionDict)

    label("Barrier width:")
    get_barrier_width = int_var(1,100000,1)
    label("Barrier height:")
    get_barrier_height = int_var(1,100000000,4)
    label("Crystal width:")
    get_crystal_width = int_var(1,100000, 1)
    label("Crystal depth:")
    get_crystal_depth = int_var(1,100000, 5)

    label("Energy:")
    get_energy = int_var(-1000000,1000000, 1)

    label("Waves:")
    waveDict = {'Cosine wave': Wf.cos_wave(), 'Gaussian': Wf.gaussian_wave(), 'Travelling gaussian': traveling_wave_fun}
    get_selected_wave = drop_down(waveDict)

    label("Initial wave offset:")
    get_wave_offset = int_var(-10000000, 10000000, 0)


    def run_simulation():
        xs = Range(get_space_divisions(), get_width())
        ts = Range(get_time_divisions(), get_max_time())
        potential = Potential.init(xs, xs.center_function(get_selected_potential()))
        psi_init = Wf.init(xs, Wf.offset(xs.center_function(get_selected_wave()), get_wave_offset()))
        psi = FiniteDifference.solve(xs, ts, potential, psi_init, get_algorithm())
        Visualize.animate_wave(xs,ts,psi)
    Button(master, text="Simulate", command=run_simulation).pack()
    master.mainloop()
