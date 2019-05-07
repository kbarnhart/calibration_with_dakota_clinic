# import modules
import sys
from subprocess import call

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from six import StringIO
from sklearn.linear_model import LinearRegression
from yaml import safe_load

from heat import BmiHeat as Heat

input_template = "input_template.yml"
inputs = "inputs.yml"

call(["dprepro", sys.argv[1], input_template, inputs])
call(['rm', input_template])

with open(inputs, "r") as f:
    params = safe_load(f)

T = params["T"]
duration_years = params["duration_years"]

surface_temperature = T * np.ones(int(np.ceil(duration_years)))

# get data, and fit a line to lower portion and estimate the thermal
# conductivity k
# dTdz = Q/k geotherm (degrees C/meter)

# k has units of J s**(-1) m**(-1) K**(-1)

# constants
seconds_per_year = 365.25 * 24 * 60 * 60
seconds_per_day = 24 * 60 * 60
Qm = 0.05  # Heat Flux W m**2 = J s m**2
rho = 2600  # Density of Rock kg m**(-3)
c = 2000  # Heat Capacity of Rock J kg**(-1) K**(-1)

path = "AWU_12AUG07.txt"
df = pd.read_csv(path, header=22, skip_blank_lines=False, sep="\s+")
deep_portion = df.Depth > 100
fit = LinearRegression().fit(
    df.Depth[deep_portion].values.reshape(-1, 1),
    df.Temperature[deep_portion].values.reshape(-1, 1),
)
k = Qm / fit.coef_[0][0]

# convert k into a thermal diffusivity
kappa = k / (rho * c)

# estimate a long term steady initial condition. Typical values are
# 30 deg per kilometer (0.03 degree per meter)
df["Temp_Init"] = fit.intercept_[0] + fit.coef_[0][0] * df.Depth

# create a 1d heat model
nrow = 20
dz = 10
file_like = StringIO(
    """
shape: [{nrow},]
spacing: [{dz},]
kappa: {kappa}
k: {k}
Qm: {Qm}
""".format(
        kappa=kappa, k=k, Qm=Qm, nrow=nrow, dz=dz
    )
)

h = Heat()
h.initialize(file_like)
h.timestep = seconds_per_day

# set the initial temperature based on our linear fit.
model_z = np.arange(0, nrow * dz, dz)
T_init = fit.intercept_[0] + fit.coef_[0][0] * model_z
h.set_value("temperature", T_init)

# run the model forward in time forced by the surface temperature.
for i in range(len(surface_temperature)):
    run_step = min([i + 1, duration_years])
    h.set_value_at_indices("temperature", [0], surface_temperature[i])
    h.update_until( run_step * seconds_per_year )

#Make a plot with initial, modeled, and final observations
# plt.figure()
# plt.plot(T_init, model_z)
# plt.plot(df.Temperature, df.Depth)
# plt.plot(h.get_value("temperature"), model_z)
# plt.gca().invert_yaxis()
# plt.ylabel("Depth [m]")
# plt.xlabel("Temperature [C]")
# plt.title("T={T}; Duration={dur}".format(T=T, dur=duration_years))
# plt.legend(["Initial Profile", "Observed", "Modeled"])
# plt.savefig("example.png")

interp_T = np.interp(df.Depth.values, model_z, h.get_value("temperature"))
#%%
# Each of the metrics listed in the Dakota .in file needs to be written to
# the specified output file given by sys.argv[2]. This is how information is
# sent back to Dakota.
with open(sys.argv[2], "w") as fp:

    # Calculate RMSE and write.
    rmse = (np.mean((interp_T - df.Temperature.values) ** 2)) ** 0.5
    fp.write(str(rmse) + "\n")
