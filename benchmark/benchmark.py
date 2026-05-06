import os
from pathlib import Path

from benchmark_utils import configure_environment, load_means, plot_grid, process_outputs


def activate_virtualenv():
    venv_path = os.path.join(os.getcwd(), "venv")
    if os.path.exists(venv_path):
        activate_script = os.path.join(venv_path, "bin", "activate_this.py")
        with open(activate_script) as f:
            exec(f.read(), {"__file__": activate_script})


def run_simulation(config_json_file="config.json"):
    import EcoSimpy

    print("Current directory:", os.getcwd())
    app_dir = os.getcwd()
    benchmark_sim = EcoSimpy.Simulation(
        app_dir,
        config_json_file,
        clean_run=True,
    )
    benchmark_sim.initialize_simulation()
    benchmark_sim.execute_simulation()


def main():
    input_dir = Path("runs")
    output_dir = Path("results")

    configure_environment()
    activate_virtualenv()
    run_simulation()
    process_outputs(input_dir, output_dir)
    household_means, cg_means = load_means(output_dir)
    plot_grid(household_means, "Household", ncol=4)
    plot_grid(cg_means, "CGFirm", ncol=4)


if __name__ == "__main__":
    main()