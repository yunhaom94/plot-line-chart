import sys

import pandas as pd
import matplotlib.pyplot as plt

def plot_lines(csv_file, ax):
    df = pd.read_csv(csv_file)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    print(df)

    for i in range(0, len(df.columns), 3):
        series_x = df.columns[i]
        series_y = df.columns[i+1]
        series_error = df.columns[i+2]
        style = df[series_y].dropna().iloc[-3:].tolist()
        x_cords = df[series_x].dropna().tolist()
        y_cords = df[series_y].dropna().iloc[:-3].tolist()
        error_values = df[series_error].dropna().tolist()
        y_cords = list(map(float, y_cords))
        error = list(map(float, error_values))
        has_style = 1
        if len(y_cords) != len(x_cords):
            y_cords = df[series_y].dropna().tolist()
            has_style = 0
        


        print("Style:")
        print(style)
        print(x_cords)
        print(y_cords)
        print(series_y)
        ax.pie(y_cords, labels=x_cords, autopct='%1.1f%%')

if __name__ == "__main__":
    csv_file1 = "results/orset_profile.csv"
    fig_file_name = "results/orset_pie.pdf"

    fig, axs  = plt.subplots(1, 1, figsize=(4.5, 2.5))
    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rcParams['legend.title_fontsize'] = 13

    plot_lines(csv_file1, axs)
    fig.savefig(fig_file_name, dpi=300, format="pdf", bbox_inches="tight")
