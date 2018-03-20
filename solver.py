import numpy as np
import math
import matplotlib.pyplot as plt


def assemble_cv_values(x, i, bc_list, h, e, b, t_star, tb, t_old, rho, c, k, dt, t_inf, t_sur):
    """
    This function calculates all the necessary values for a given cv
    :return: Ap, Aw, Ae, b
    """

    dx_ww, dx_we, dx_ew, dx_ee, bc = get_cv_geometry(x, i, bc_list)
    sc, sp = get_sources(h, e, b, t_star, t_inf, t_sur)

    dx = (dx_we + dx_ew)

    if bc == 'fixed':

        ap = 1
        aw = 0
        ae = 0
        b = tb

    elif bc == 'adiabatic':

        aw = k / (dx_ww+dx_we)
        ae = 0.
        ap_o = rho*c*dt/dx
        b = sc*dx + ap_o*t_old
        ap = ae + aw + ap_o - sp * dx

    else:

        aw = k / (dx_ww + dx_we)
        ae = k / (dx_ee+dx_ew)
        ap_o = rho * c * dt / dx
        b = sc * dx + ap_o * t_old
        ap = ae + aw + ap_o - sp * dx

    return ap, aw, ae, b


def get_sources(h, e, b, t_star, t_inf, t_sur):

    sigma = 0.0000000567
    sp = -2.*(h+e*sigma*4.*math.pow(t_star, 3.))/b
    sc = 2.*(h*t_inf+e*sigma*(4.*math.pow(t_star, 4.)+math.pow(t_sur, 4.)))/b
    return sc, sp


def get_cv_geometry(x, i, bc_list):

    if i == 0:
        bc = bc_list[0]

        bdx = (x[i+1]-x[i])/2

        dx_ww = 0
        dx_we = 0
        dx_ew = bdx
        dx_ee = x[i + 1] - x[i] - bdx

    elif i == len(x)-1:
        bc = bc_list[1]

        bdx = (x[i]-x[i-1])/2

        dx_ww = x[i] - x[i-1] - bdx
        dx_we = bdx
        dx_ew = 0
        dx_ee = 0

    else:
        bc = None

        bdx = (x[i] - x[i - 1])

        dx_ww = x[i] - x[i-1] - bdx / 2
        dx_we = x[i] - x[i-1] - dx_ww
        dx_ee = x[i+1] - x[i] - bdx / 2
        dx_ew = x[i+1] - x[i] - dx_ee

    return [dx_ww, dx_we, dx_ew, dx_ee, bc]


def mat(x, bc_list, h, e, b, t_star, tb, t_old, rho, c, k, dt, t_inf, t_sur):

    a_mat = np.zeros((len(x), len(x)), dtype=float)
    b_mat = np.zeros((len(x), 1), dtype=float)

    # loop over each node
    for i in xrange(len(x)):

        # get cv values
        ap, aw, ae, bp = assemble_cv_values(x, i, bc_list, h, e, b, t_star, tb, t_old, rho, c, k, dt, t_inf, t_sur)

        # assemble into mat
        a_mat[i, i] = ap
        b_mat[i] = bp

        if aw != 0:
            a_mat[i, i - 1] = -aw
        if ae != 0:
            a_mat[i, i + 1] = -ae

    # solve mat equation
    a = np.matrix(a_mat)
    b = np.matrix(b_mat)

    return a.I * b


def solve(l, dx, bc_list, t_init, t_stop, dt, k, c, rho, tb, b, e, h, t_inf, t_sur, plt_f=False, crt=0.0001):

    """
    This function assembles A and b then solves for T (AT = b)
    :param l: domain length
    :type dx: float
    :param dx: grid size
    :type dx: float
    :param bc_list: [boundary condition 1, boundary condition 2]
    :type bc_list: [dict, dict]
    :param t_init: initial temperature
    :type t_init: float
    :param t_stop: final solution time
    :type t_stop: float
    :param dt: time step size
    :type dt: float
    :param k: conduction coefficient
    :type k: float
    :param c: thermal properties
    :type c: float
    :param rho: density
    :type rho: float
    :param tb: boundary temperature
    :type tb: float
    :param b: thickness
    :type b: float
    :param e: emissivity
    :type e: float
    :param h: heat transfer coefficient
    :type h: float
    :param t_inf: free temperature
    :type t_inf: float
    :param t_sur: surrounding temperature
    :type t_sur: float
    :param plt_f: indicator to plot
    :type plt_f: bool
    :param crt: convergence criterion
    :type crt: float
    :return: iterable, T
    """

    x = np.linspace(0., l, int(l / dx))

    # Set Initials
    t = np.ones(x.shape)*t_init
    t_star = np.copy(t)
    t_old = np.copy(t)

    if plt_f:
        fig, line = create_plotter(x, t)
    else:
        fig, line = [None, None]

    # Loop over time
    for i in xrange(int(t_stop/dt)):

        # Loop while
        while max(np.absolute(t_star-t)) > crt:

            # solve t
            t = mat(x, bc_list, h, e, b, t_star, tb, t_old, rho, c, k, dt, t_inf, t_sur)

            # set t _ star
            t_star = np.copy(t)

            # update
            if plt_f:
                update_plots(fig, line, t)

        t_old = t

    return np.asarray(t)


def update_plots(fig, line, new_data):
    line.set_ydata(new_data)
    fig.canvas.draw()


def create_plotter(x, t):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line, = ax.plot(x, t)
    return fig, line
