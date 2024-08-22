import sys

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

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
        x_cords = list(map(float, x_cords))
        y_cords = list(map(float, y_cords))
        error = list(map(float, error_values))
        has_style = 1
        if len(y_cords) != len(x_cords):
            y_cords = df[series_y].dropna().tolist()
            has_style = 0
        # print("X:")
        # print(x_cords)
        # print("Y:")
        # print(y_cords)
        # print("Error:")
        # print(error)
        
        if has_style:
            print("Style:")
            print(style)

            ax.plot(x_cords, y_cords, label=series_y, linestyle=style[0], color=style[2])

        else:
            raise Exception("No style provided")

    
    for l in ax.lines:
        l.set_linewidth(0.9)
        l.set_alpha(0.7)


    ax.grid(True)
    ax.set_xlim(left=0, right=500)
    
    ax.set_ylabel("Latency (ms)", fontsize=13)
    ax.set_xlabel("% of Elapsed Time", fontsize=13)

    
    ax.set_yscale('log')

    #ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0), useMathText=True)
    legend = ax.legend(bbox_to_anchor=(0.55, 1.38), ncol=1, loc='upper center', fontsize=13, columnspacing=0.5) 
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=500))

  
if __name__ == "__main__":
    csv_file1 = "results/ts.csv"
    fig_file_name = "results/ts.pdf"

    fig, axs  = plt.subplots(1, 1, figsize=(4, 3.5))
    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rcParams['legend.title_fontsize'] = 13

    plot_lines(csv_file1, axs)
    fig.savefig(fig_file_name, dpi=300, format="pdf", bbox_inches="tight")
