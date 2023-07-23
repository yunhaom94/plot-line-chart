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
    group_width = 1 # change this will change the overall fatness of the group chart
    first_col = df[df.columns[0]].dropna()
    x = np.arange(len(first_col))
    width = group_width / len(first_col)
    print(width)
    i = 0
    for series_y in df.columns:
        if series_y == df.columns[0]:
            continue
        # all y shares the same x axis str entries
        series_x = df.columns[0]
        style = df[series_y].dropna().iloc[-1:].tolist()
        x_labels = df[series_x].dropna().tolist()
        y_cords = df[series_y].dropna().iloc[:-1].tolist()
        y_cords = list(map(float, y_cords))
        has_style = 1
        if len(y_cords) != len(x_labels):
            y_cords = df[series_y].dropna().tolist()
            has_style = 0
        print("X:")
        print(x_labels)
        print("Y:")
        print(y_cords)
        if has_style:
            print("Style:")
            print(style)

        if has_style:
            plt.bar(x - width + width * i, y_cords, width, label=series_y, color=style[0])
        else:
            plt.bar(x - width + width * i, y_cords, width, label=series_y)

        i += 1

    # there are more to the loc, placing it outside the chat is more complex
    plt.xticks(x, first_col)
    plt.legend(loc='best')
    plt.grid(True)
    #plt.gca().set_xlim(0, 6)
    #plt.gca().set_ylim(0, 10)
    #plt.show()
    plt.savefig(fig_file_name)

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
