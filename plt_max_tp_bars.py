import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_bars(csv_file, ax, left_or_right):
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
                ax.bar(x - width * 2 + width * (i/2), y_cords, width, label=label, hatch=style[0], edgecolor=style[1],  fill=False)
                ax.errorbar(x - width * 2 + width * (i/2), y_cords, yerr=error, color=style[1], ls='none', capsize=2)
            else:
                raise Exception("No style provided")

        i += 1


    #ax.set_box_aspect(1)

    # there are more to the loc, placing it outside the chat is more complex
    ax.set_xticks(x, first_col, fontsize=12)

    if (left_or_right == 0):
        ax.set_title("PN-Counter", y=1, size=15)
        ax.set_ylabel("Throughput (ops/s)", fontsize=13)
        ax.set_yticks([100000, 200000, 300000, 400000])
        
    else:
        ax.set_title("OR-Set", y=1, size=15)
        ax.set_yticks([30000, 60000, 90000, 120000])

    ax.legend(loc='upper right')
    ax.grid(True)

    #ax.set_xlim(left=-0.5)
    ax.set_ylim(bottom=0)


    ax.set_xlabel("Access Pattern", fontsize=13)
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0), useMathText=True)
    
    
if __name__ == "__main__":
    csv_file1 = "results/pnc_max_tp.csv"
    csv_file2 = "results/orset_max_tp.csv"
    fig_file_name = "results/max_tp.pdf"

    fig, axs  = plt.subplots(1, 2, figsize=(8.3, 4))


    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rc('figure', titlesize=20)  # fontsize of the figure title

    plot_bars(csv_file1, axs[0], 0)
    plot_bars(csv_file2, axs[1], 1)


    plt.subplots_adjust(wspace=0.15, hspace=0.1)
    fig.savefig(fig_file_name, dpi=300, format="pdf", bbox_inches="tight")