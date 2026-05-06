import os
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

sns.set_theme(style="whitegrid")
pd.options.mode.chained_assignment = None

input_dir  = Path("runs")
output_dir = Path("results")
output_dir.mkdir(exist_ok=True)
import EcoSimpy


print("Current directory:", os.getcwd())

config_json_file = "config.json"
app_dir = os.getcwd()

sim = EcoSimpy.Simulation(app_dir,
                            config_json_file,
                            clean_run=True)
sim.initialize_simulation()
sim.execute_simulation()

