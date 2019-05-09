# Import  modules
import sys
from subprocess import call

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from six import StringIO
from sklearn.linear_model import LinearRegression
from scipy.interpolate import interp1d
from yaml import safe_load

from heat import BmiHeat as Heat

# Set physical constants
seconds_per_year = 365.25 * 24 * 60 * 60
seconds_per_day = 24 * 60 * 60
Qm = 0.05  # Heat Flux W m**2 = J s m**2
rho = 2600  # Density of Rock kg m**(-3)
c = 2000  # Heat Capacity of Rock J kg**(-1) K**(-1)

#########################################
#                                       #
#    Step 1: Use Dakota created         #
#    input files to prepare for         #
#    model run.                         #
#                                       #
#########################################
input_template = "input_template.yml"
inputs = "inputs.yml"
call(["dprepro", sys.argv[1], input_template, inputs])
call(['rm', input_template])

#########################################
#                                       #
#    Step 2: Run Model                  #
#                                       #
#########################################
# Load parameters from the yaml formatted input.
with open(inputs, "r") as f:
    params = safe_load(f)
    T = params["T"]
    duration_years = params["duration_years"]

# Create our model for surface  temperature.  Later on in the clinic, consider
# making this more complicated.
surface_temperature = interp1d([0, duration_years], [T, T])

# Open a file from Clow (2014, and fit a line to lower portion and estimate the
# thermal conductivity k
# Note that dTdz = Q/k (dTdz is the geotherm with units of [degrees C/meter])
# k has units of [J s**(-1) m**(-1) K**(-1)]

path = "AWU_12AUG07.txt"
df = pd.read_csv(path, header=22, skip_blank_lines=False, sep="\s+")
deep_portion = df.Depth > 100
fit = LinearRegression().fit(
    df.Depth[deep_portion].values.reshape(-1, 1),
    df.Temperature[deep_portion].values.reshape(-1, 1),
)

# Estimate k the thermal conductivity, given the gradient and Qm.
k = Qm / fit.coef_[0][0]

# Given a density and a heat capacity, convert k into a thermal diffusivity.
kappa = k / (rho * c)

# Create an input file for a 1d Heat model
file_like = StringIO(
    """
shape: [20,]
spacing: [10,]
kappa: {kappa}
k: {k}
Qm: {Qm}
""".format(
        kappa=kappa, k=k, Qm=Qm
    )
)

# Create an instance of the Heat model, initialize it from the file.
h = Heat()
h.initialize(file_like)

# set the initial temperature based on our linear fit.
model_z = np.arange(0, nrow * dz, dz)
T_init = fit.intercept_[0] + fit.coef_[0][0] * model_z
h.set_value("temperature", T_init)

# override the default timestep to use 1 day.
h.timestep = seconds_per_day

# run the model forward in time forced by the surface temperature.
while h.get_model_time() < duration_years * seconds_per_year:
    # calculate the time to run until.
    run_until = min([h.get_model_time() + seconds_per_year,
                     duration_years*seconds_per_year])
    # determine the current surface temperature
    current_time = h.get_model_time()/seconds_per_year
    current_surface_temperature = surface_temperature(current_time)
    # set the surface temperature in the model.
    h.set_value_at_indices("temperature", [0], current_surface_temperature)
    # run forward in time.
    h.update_until(run_until)

#########################################
#                                       #
#    Step 3: Write Output in format     #
#    Dakota expects                     #
#                                       #
#########################################

# Each of the metrics listed in the Dakota .in file needs to be written to
# the specified output file given by sys.argv[2]. This is how information is
# sent back to Dakota.

# Calculate the root mean squared error (rmse)
interp_T = np.interp(df.Depth.values, model_z, h.get_value("temperature"))
rmse = (np.mean((interp_T - df.Temperature.values) ** 2)) ** 0.5

# Write it to the expected file.
with open(sys.argv[2], "w") as fp:
    fp.write(str(rmse))
