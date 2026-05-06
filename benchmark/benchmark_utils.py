import math
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def configure_environment():
    sns.set_theme(style="whitegrid")
    pd.options.mode.chained_assignment = None


def process_outputs(input_dir, output_dir):
    output_dir.mkdir(exist_ok=True)
    print(input_dir)

    files = [f for f in os.listdir(input_dir) if "macro_model_Household" in f]
    if files:
        household = pd.read_csv(os.path.join(input_dir, files[0]))
        household = household.drop(columns=[col for col in ["run", "index_no"] if col in household.columns])
    else:
        household = pd.DataFrame()

    files = [f for f in os.listdir(input_dir) if "macro_model_CGFirm" in f]
    if files:
        cg_firm = pd.read_csv(os.path.join(input_dir, files[0]))
        cg_firm = cg_firm.drop(columns=[col for col in ["run", "index_no"] if col in cg_firm.columns])
    else:
        cg_firm = pd.DataFrame()

    if not household.empty:
        household_means = household.groupby("step").agg(
            {
                **{col: "mean" for col in household.select_dtypes(include="number").columns if col != "step"},
                **{col: "sum" for col in household.select_dtypes(include="bool").columns},
            }
        ).reset_index()
        household_means.to_csv(output_dir / "household_means.csv", index=False)
    else:
        print("Nenhum dado Household encontrado.")

    if not cg_firm.empty:
        cg_means = cg_firm.groupby("step").agg(
            {
                **{col: "mean" for col in cg_firm.select_dtypes(include="number").columns if col != "step"},
                **{col: "sum" for col in cg_firm.select_dtypes(include="bool").columns},
            }
        ).reset_index()
        cg_means.to_csv(output_dir / "cg_means.csv", index=False)
    else:
        print("Nenhum dado CGFirm encontrado.")

    print("Processamento concluído.")


def load_means(output_dir):
    household_means_path = output_dir / "household_means.csv"
    cg_means_path = output_dir / "cg_means.csv"

    if household_means_path.exists():
        household_means = pd.read_csv(household_means_path)
    else:
        household_means = None
        print("Arquivo household_means.csv não encontrado.")

    if cg_means_path.exists():
        cg_means = pd.read_csv(cg_means_path)
    else:
        cg_means = None
        print("Arquivo cg_means.csv não encontrado.")

    return household_means, cg_means


def plot_grid(df, title_prefix, ncol=4):
    if df is None:
        return
    cols = [col for col in df.columns if col != "step"]
    n = len(cols)
    nrow = math.ceil(n / ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(5 * ncol, 3 * nrow), squeeze=False)
    for idx, var in enumerate(cols):
        ax = axes[idx // ncol][idx % ncol]
        ax.plot(df["step"], df[var], marker="o", linewidth=1)
        ax.set_title(f"{title_prefix} - {var}", fontsize=10)
        ax.set_xlabel("Step", fontsize=8)
        ax.set_ylabel(f"means - {var}", fontsize=8)
        ax.grid(True, alpha=0.3)
    for idx in range(n, nrow * ncol):
        fig.delaxes(axes[idx // ncol][idx % ncol])
    plt.tight_layout()
    plt.show()