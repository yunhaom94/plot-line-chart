import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_bars(csv_file, axs):
    df = pd.read_csv(csv_file)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    print(df)
    # Create a new plot

    group_width = 0.7 # change this will change the overall fatness of the group chart
    first_col = df[df.columns[0]].dropna()
    x = np.arange(len(first_col))
    width = group_width / len(first_col)
    print(width)
    i = 1

    series_x = df.columns[0]
    x_labels = df[series_x].dropna().tolist()
    for series_y in df.columns:
        print(i)
        
        if series_y == df.columns[0]:
            continue
        # all y shares the same x axis str entries
        
        # odd column are y values
        if (i % 2 == 1):
            print("y:" + series_y)
            label = series_y
            style = df[series_y].dropna().iloc[-2:].tolist()
            y_cords = df[series_y].dropna().iloc[:-2].tolist()
            y_cords = list(map(float, y_cords))
            
            has_style = 1
            if len(y_cords) != len(x_labels):
                y_cords = df[series_y].dropna().tolist()
                has_style = 0

        # even column are error values, and draw the bar when it is even    
        elif (i % 2 == 0):
            print("err:" + series_y)
            error = df[series_y].dropna().tolist()
            error = list(map(float, error))

            print("X:")
            print(x_labels)
            print("Y:")
            print(y_cords)
            if has_style:
                print("Style:")
                print(style)

            if has_style:
                axs.bar(x - width * 2 + width * (i/2), y_cords, width, label=label, hatch=style[0], edgecolor=style[1],  fill=False)
                axs.errorbar(x - width * 2 + width * (i/2), y_cords, yerr=error, color=style[1], ls='none', capsize=2)
            else:
                raise Exception("No style provided")

        i += 1

    axs.set_xticks(x, first_col)
    axs.grid(True)
    axs.set_yscale("log")
    axs.set_box_aspect(1)
    axs.legend(title="Sending Rate (TPS)")
    axs.set_xlabel("Transaction Type", fontsize=13)
    axs.set_ylabel("Latency (ms)", fontsize=13)
    axs.set_title(None)


if __name__ == "__main__":
    csv_file1 = "results/bank_lt_vs_type.csv"
    fig_file_name = "results/bank_lt_vs_type.pdf"
    
    fig, axs  = plt.subplots(1, 1, figsize=(4.5, 4.5))
    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rcParams['legend.title_fontsize'] = 13

    plot_bars(csv_file1, axs)
    fig.savefig(fig_file_name, dpi=300, format="pdf", bbox_inches="tight")
