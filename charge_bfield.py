# This code creates a visualization of the magnetic field around a moving point charge. It uses the module vpython to create the images and implements the Biot-Savart law.

from vpython import *
from math import *

# params
dt = 0.1
Nmax = 20000
vel = vec(5, 0, 0)  # m/s
L = 100
dL = 20
Barrow_scale = 30


# physical constants
q = 1.609e-19  # C
c = 3e8  # m/s
mu0 = 4 * pi * 1e-7
mu0q_over_4pi = mu0 * q / (4 * pi)
Bscale = mu0q_over_4pi * vel.mag / (dL * dL)

# axes
origin = vec(0, 0, 0)
axis_headwidth = 5
axis_headlength = 5
axis_shaftwidth = 1
axis_params = {
    "pos": origin,
    "headwidth": axis_headwidth,
    "headlength": axis_headlength,
    "shaftwidth": axis_shaftwidth,
    "round": True,
}
xaxispos = arrow(axis=vec(L, 0, 0), **axis_params)
xaxisneg = arrow(axis=vec(-L, 0, 0), **axis_params)
yaxispos = arrow(axis=vec(0, L, 0), **axis_params)
yaxisneg = arrow(axis=vec(0, -L, 0), **axis_params)
zaxispos = arrow(axis=vec(0, 0, L), **axis_params)
zaxisneg = arrow(axis=vec(0, 0, -L), **axis_params)


# build initial field
bfield = []
numarrow = ceil(2 * L / dL) + 1
bfield_axis_headwidth = 2
bfield_axis_headlength = 2
bfield_axis_shaftwidth = 1
bfield_start_axis = vec(1e-5, 0, 0)  # Must start from non-zero value to avoid bugs

for i in range(numarrow):

    for j in range(numarrow):

        for k in range(numarrow):

            next_pos = vec(-L + dL * i, -L + dL * j, -L + dL * k)
            next_arrow = arrow(
                pos=next_pos,
                axis=bfield_start_axis,
                round=True,
                headwidth=bfield_axis_headwidth,
                headlength=bfield_axis_headlength,
                shaftwidth=bfield_axis_shaftwidth,
                color=color.cyan,
            )
            bfield.append(next_arrow)

# The point charge
charge_rad = 3
charge_col = color.red
charge = sphere(pos=vec(-L, 0, 0), radius=charge_rad, color=charge_col)
vel_scale = 20
vel_headwidth = 5
vel_headlength = 3
vel_shaftwidth = 3
velarrow = arrow(
    pos=charge.pos,
    axis=vel_scale * vel.hat,
    round=True,
    headwidth=vel_headwidth,
    headlength=vel_headlength,
    shaftwidth=vel_shaftwidth,
    color=color.orange,
)

# Time loop
n = 0
while n < Nmax:

    n += 1
    charge.pos += vel * dt
    velarrow.pos = charge.pos

    # Update magnetic field
    for point in bfield:

        rf = point.pos
        rs = charge.pos
        r = rf - rs
        rmag = r.mag

        if rmag > 0:
            rhat = r / rmag
            B = mu0q_over_4pi * cross(vel, rhat) / (rmag * rmag)
            B_scaled = (B / Bscale) * Barrow_scale

            factor = B_scaled.mag

            # Update properties of the existing arrow in-place
            point.axis = B_scaled
            point.headwidth = 0.5 * factor
            point.headlength = 0.5 * factor
            point.shaftwidth = 0.25 * factor

    if abs(charge.pos.x) > L:

        vel *= -1
        velarrow.axis *= -1

    rate(500)
