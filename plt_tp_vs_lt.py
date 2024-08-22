import sys
from matplotlib.ticker import ScalarFormatter

import pandas as pd
import matplotlib.pyplot as plt


def plot_lines(csv_file, ax, left_or_right):
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
        x_cords = list(map(float, x_cords))
        y_cords = list(map(float, y_cords))
        error = list(map(float, error_values))
        has_style = 1
        if len(y_cords) != len(x_cords):
            y_cords = df[series_y].dropna().tolist()
            has_style = 0
        print("X:")
        print(x_cords)
        print("Y:")
        print(y_cords)
        print("Error:")
        print(error)
        

        if has_style:
            print("Style:")
            print(style)

            ax.plot(x_cords, y_cords, label=series_y, linestyle=style[0], marker=style[1], color=style[2])
            ax.errorbar(x_cords, y_cords, yerr=error, linestyle=style[0], marker=style[1], color=style[2], capsize=2, elinewidth=0.5)

        else:
            raise Exception("No style provided")
        # set aspect ratio
    
    for l in ax.lines:
        l.set_linewidth(0.9)
        l.set_alpha(0.7)


    ax.grid(True)
    ax.set_xlim(left=0)
    ax.set_xlabel("Throughput (ops/s)", fontsize=9)
    ax.set_ylim(bottom=0)

    if (left_or_right == 0):
        legend = ax.legend(bbox_to_anchor=(1.05, 1.42), ncol=5, loc='upper center', fontsize=10) 
        ax.set_ylabel("Latency (ms)", fontsize=9)
        ax.set_title("PN-Counter", y=1, size=9)

        ax.set_xticks([100000, 200000, 300000, 400000])

    if (left_or_right == 1):
        ax.set_title("OR-Set", y=1, size=9)
        ax.set_ylim(top=8000)
        ax.set_xticks([40000, 80000, 120000, 160000, 200000])

    ax.ticklabel_format(style='scientific', axis='x', scilimits=(0,0), useMathText=True)




# Apply the custom formatter to the x-axis



if __name__ == "__main__":
    csv_file1 = "results/pnc_tp_vs_lt.csv"
    csv_file2 = "results/orset_tp_vs_lt.csv"
    fig_file_name = "results/tp_vs_lt.pdf"

    fig, axs  = plt.subplots(1, 2, figsize=(12, 2.2))

    plot_lines(csv_file1, axs[0], 0)
    plot_lines(csv_file2, axs[1], 1)

    plt.subplots_adjust(wspace=0.15, hspace=0)
    fig.savefig(fig_file_name, dpi=300, format="pdf", bbox_inches="tight")