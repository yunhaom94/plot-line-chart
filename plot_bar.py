import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_line_segments(csv_file, fig_file_name):
    df = pd.read_csv(csv_file)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    print(df)
    # Create a new plot
    plt.figure()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Bar Segment Chart')
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
                plt.bar(x - width * 2 + width * (i/2), y_cords, width, label=label, hatch=style[0], edgecolor=style[1],  fill=False)
                plt.errorbar(x - width * 2 + width * (i/2), y_cords, yerr=error, color=style[1], ls='none', capsize=2)
            else:
                plt.bar(x - width * 2 + width * (i/2), y_cords, width, label=label)

        i += 1

    # there are more to the loc, placing it outside the chat is more complex
    plt.xticks(x, first_col)
    plt.legend(loc='best')
    plt.grid(True)
    plt.yscale("log")
    #plt.gca().set_xlim(0, 6)
    #plt.gca().set_ylim(0, 10)
    #plt.show()

    # plt.xlabel("Access Pattern")
    # plt.ylabel("Throughput (ops/s)")
    plt.legend(title="Sending Rate (ops/s)")
    plt.xlabel("Transaction Type")
    plt.ylabel("Latency (ms)")
    plt.title(None)

    plt.savefig(fig_file_name, dpi=300)

if __name__ == "__main__":
    # read arg 1 as csv file name if arg 2 is not given use the input as the save file name (change extension to .png)
    if len(sys.argv) == 2:
        csv_file_name = sys.argv[1]
        save_file_name = csv_file_name.split('.')[0] + '.png'
        plot_line_segments(csv_file_name, save_file_name)
    elif len(sys.argv) == 3:
        plot_line_segments(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python plot.py <csv_file_name> <save_file_name>")
