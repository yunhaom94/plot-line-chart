import sys

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
    plt.title('Line Segment Chart')
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

            plt.plot(x_cords, y_cords, label=series_y, linestyle=style[0], marker=style[1], color=style[2])
            plt.errorbar(x_cords, y_cords, yerr=error, linestyle=style[0], marker=style[1], color=style[2], capsize=2, elinewidth=0.5)


        else:
            plt.plot(x_cords, y_cords, label=series_y)
            plt.errorbar(x_cords, y_cords, yerr=error)
        
        # set aspect ratio

        

    # there are more to the loc, placing it outside the chat is more complex
    for l in plt.gca().lines:
        l.set_linewidth(0.9)
        l.set_alpha(0.7)
           
    plt.legend(bbox_to_anchor=(0.5, 1.16), ncol=3, loc='upper center')    
    plt.grid(True)
    plt.gca().set_xlim(left=0)
    plt.gca().set_ylim(bottom=0)
    #plt.gca().set_ylim(bottom=800, top=1600)
    #plt.yscale("log")
    #plt.show()

    # plt.xlabel("Sending Rate (ops/s)")
    plt.xlabel("# of Nodes")
    #plt.ylabel("Latency (ms)")
    plt.ylabel("Throughput (ops/s)")
    plt.title(None)


    plt.savefig(fig_file_name, dpi=300)
    #plt.savefig(fig_file_name, dpi=300, format="pdf", bbox_inches="tight")

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
