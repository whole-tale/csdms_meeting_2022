# Plotting grid data with Landlab based on 
# https://landlab.readthedocs.io/en/latest/user_guide/tutorials.html

import numpy as np
from landlab import RasterModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder, ChannelProfiler
from matplotlib.pyplot import title, figure, savefig

mg = RasterModelGrid((100, 100), 1000.0)
mg.axis_units = ("m", "m")
z = mg.add_zeros("topographic__elevation", at="node")
z += np.random.rand(mg.number_of_nodes)  # roughen the initial surface

fr = FlowAccumulator(mg)
sp = FastscapeEroder(mg, K_sp=1.0e-5)
dt = 50000.0

for ndt in range(100):
    z[mg.core_nodes] += 10.0
    fr.run_one_step()
    sp.run_one_step(dt)
    if ndt % 5 == 0:
        print(ndt)

prf = ChannelProfiler(
    mg, number_of_watersheds=4, main_channel_only=False, minimum_channel_threshold=1e7
)
prf.run_one_step()

prf.plot_profiles()
savefig("figures/figure1.png")

prf.plot_profiles_in_map_view()
savefig("figures/figure2.png")