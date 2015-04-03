import numpy

class Range:
    def __init__(self, num_divisions, x_max):
        indicies = numpy.arange(num_divisions)
        ind_to_x = lambda i: numpy.interp(i,[0,num_divisions],[0,x_max])
        self.values = ind_to_x(indicies)
        self.x_max = x_max
        self.num_divisions = num_divisions
        self.delta = float(x_max) / num_divisions

    def get_max(self):
        return self.x_max

    def get_delta(self):
        return self.delta

    def get_values(self):
        return self.values

    def get_num_divisions(self):
        return self.num_divisions