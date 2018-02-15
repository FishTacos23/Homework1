# This is a 1D CFD Thermal Solver using Practice B
import matplotlib.pyplot as plt
import math
import numpy as np
import solver
import p3


def exact_study(num_cv_list, x_dist_max, bc_list, p, exact, max_cv):

    max_temp = []

    def get_temps(num):

        cv_boundaries = [it * x_dist_max / float(num) for it in xrange(num + 1)]  # x boundary locations
        node_properties = [0 if y <= 0.030000000001 else 1 for y in cv_boundaries]
        node_properties.append(1)

        temps, x_dist = solver.solve(cv_boundaries, bc_list, p, node_properties)
        max_temp.append(temps.max())

    get_temps(num_cv_list[-1])
    num_cv_list.append(num_cv_list[-1]*2)
    get_temps(num_cv_list[-1])

    while num_cv_list[-1] < max_cv:

        num_cv_list.append(num_cv_list[-1]*2)
        get_temps(num_cv_list[-1])

    print num_cv_list
    print max_temp

    diff_temps = []
    exact_x = []
    exact_y = []

    for i in xrange(len(max_temp)):
        diff_temps.append((exact-max_temp[i])/exact)
        exact_x.append(num_cv_list[i])
        exact_y.append(exact)
    print diff_temps

    plt.semilogx(exact_x, exact_y, 'r--')
    plt.semilogx(num_cv_list, max_temp)
    plt.show()


def convergence_study(num_cv_list, x_dist_max, bc_list, p, crit):

    max_temp = []
    exact = 588.117139215064

    def get_temps(num):

        cv_boundaries = [it * x_dist_max / float(num) for it in xrange(num + 1)]  # x boundary locations
        node_properties = [0 if y <= 0.030000000001 else 1 for y in cv_boundaries]
        node_properties.append(1)

        temps, x_dist = solver.solve(cv_boundaries, bc_list, p, node_properties)
        max_temp.append(temps.max())

    get_temps(num_cv_list[-1])
    num_cv_list.append(num_cv_list[-1]*2)
    get_temps(num_cv_list[-1])

    while abs(max_temp[-1]-max_temp[-2]) > crit:

        num_cv_list.append(num_cv_list[-1]*2)
        get_temps(num_cv_list[-1])

    print num_cv_list
    print max_temp
    plt.plot(num_cv_list, max_temp)
    plt.show()


def prob3():
    p3.solve()


def prob4():

    # properties dictionary
    prop1 = {'k': lambda x: 15, 'q': 4000000}
    prop2 = {'k': lambda x: 60, 'q': 0}

    # This variable contains a set of properties for any given segment
    properties = [prop1, prop2]

    # use for equally spaced control volumes
    num_cvs = 20
    x_max = 0.05
    cv_boundaries = [it * x_max / float(num_cvs) for it in xrange(num_cvs + 1)]  # x boundary locations
    node_properties = [0 if y <= 0.030000000001 else 1 for y in cv_boundaries]
    node_properties.append(1)

    # This variable contains the boundary conditions
    bound_i = {'type': 'insulated'}
    bound_c = {'type': 'convective', 'h': 1000, 'To': 300}
    boundaries = [bound_i, bound_c]

    py, px = solver.solve(cv_boundaries, boundaries, properties, node_properties)

    plt.plot(px, py)
    plt.show()


def prob5ab():
    # properties dictionary
    prop1 = {'k': lambda x: 15, 'q': 4000000}
    prop2 = {'k': lambda x: 137 * math.exp(25 * x - 2), 'q': 0}

    # This variable contains a set of properties for any given segment
    properties = [prop1, prop2]

    # use for equally spaced control volumes
    num_cvs = 20
    x_max = 0.05
    cv_boundaries = [it * x_max / float(num_cvs) for it in xrange(num_cvs + 1)]  # x boundary locations
    node_properties = [0 if y <= 0.030000000001 else 1 for y in cv_boundaries]
    node_properties.append(1)

    # This variable contains the boundary conditions
    bound_i = {'type': 'insulated'}
    bound_c = {'type': 'convective', 'h': 1000, 'To': 300}
    boundaries = [bound_i, bound_c]

    py, px = solver.solve(cv_boundaries, boundaries, properties, node_properties)

    plt.plot(px, py)
    plt.show()


def prob5c():

    # properties dictionary
    prop1 = {'k': lambda x: 15, 'q': 4000000}
    prop2 = {'k': lambda x: 137 * math.exp(25 * x - 2), 'q': 0}

    # This variable contains a set of properties for any given segment
    properties = [prop1, prop2]

    x_max = 0.05

    # This variable contains the boundary conditions
    bound_i = {'type': 'insulated'}
    bound_c = {'type': 'convective', 'h': 1000, 'To': 300}
    boundaries = [bound_i, bound_c]

    # for grid convergence study
    number_control_volumes = [5]
    crt = 0.001
    convergence_study(number_control_volumes, x_max, boundaries, properties, crt)


def prob1():

    exact = 588.117139215064
    max_cv = 10240

    # properties dictionary
    prop1 = {'k': lambda x: 15, 'q': 4000000}
    prop2 = {'k': lambda x: 137 * math.exp(25 * x - 2), 'q': 0}

    # This variable contains a set of properties for any given segment
    properties = [prop1, prop2]

    x_max = 0.05

    # This variable contains the boundary conditions
    bound_i = {'type': 'insulated'}
    bound_c = {'type': 'convective', 'h': 1000, 'To': 300}
    boundaries = [bound_i, bound_c]

    # for grid convergence study
    number_control_volumes = [5]
    exact_study(number_control_volumes, x_max, boundaries, properties, exact, max_cv)


def prob2():

    tolerance = 0.0001

    # geometry basics
    x_max = 0.02
    number_control_volumes = 5

    # This variable contains a set of properties for any given segment
    prop1 = {'k': lambda x: 401, 'h': 1000, 'e': 0, 'T': 273, 'D': 0.003}
    properties = [prop1]

    cv_boundaries = [it * x_max / float(number_control_volumes) for it in xrange(number_control_volumes + 1)]
    node_properties = [0]*(number_control_volumes+1)
    node_properties.append(0)

    # This variable contains the boundary conditions
    bound_i = {'type': 'fixed', 'T': 400}
    bound_c = {'type': 'convective_radiative', 'h': 10, 'e': 0, 'T': 273}
    boundaries = [bound_i, bound_c]

    temperature_diffs = np.ones(number_control_volumes+2, dtype=float)
    temperature_prev = np.ones(number_control_volumes+2, dtype=float)*400.

    total_temps = [temperature_prev]
    x_pos = None

    # iterate until temperature convergence is reached
    while temperature_diffs.max() > tolerance:

        # calculate temperatures
        temperature_current, x_pos = solver.solve(cv_boundaries, boundaries, properties, node_properties,
                                                  temperature_prev)

        # get difference
        temperature_diffs = np.absolute(temperature_current-temperature_prev)

        # set previous
        temperature_prev = temperature_current

        total_temps.append(temperature_prev)

    exact = []
    t_inf = prop1['T']
    t_b = bound_i['T']
    n = math.sqrt(4.*prop1['h']/(prop1['k'](1.)*prop1['D']))

    for x_v in x_pos:
        t_act = (t_b-t_inf)*math.cosh(n*(x_max-x_v))/math.cosh(n*x_max)+t_inf
        exact.append(t_act)

    # for plotting final temperature vs exact temperature
    plt.plot(x_pos, temperature_prev, 'b')
    plt.plot(x_pos, exact, 'r--')
    plt.show()

    # # For plotting every iteration of temperature
    # for temp in total_temps:
    #     plt.plot(x_pos, temp)
    # plt.show()


if __name__ == '__main__':

    prob2()
