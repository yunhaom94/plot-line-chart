import sys
import matplotlib
from matplotlib.ticker import StrMethodFormatter

import pandas as pd
import matplotlib.pyplot as plt

def plot_lines(csv_file, ax, row, column):
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
    #ax.set_box_aspect(1)
    #ax.set_xlim(left=0)
    
    #ax.set_ylim(bottom=0)

    if (row == 0 and column == 0):
        ax.set_title("PN-Counter", y=1, size=15)
        ax.set_ylabel("Throughput (ops/s)", fontsize=13)
        ax.set_yticks([80000, 160000, 240000])
        legend = ax.legend(bbox_to_anchor=(1.05, 1.45), ncol=3, loc='upper center') 
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0), useMathText=True)
        ax.set_xticklabels([])

        
    elif (row == 0 and column == 1):
        ax.set_title("OR-Set", y=1, size=15)
        ax.set_yticks([30000, 60000, 90000])

        class OOMFormatter(matplotlib.ticker.ScalarFormatter):
            def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
                self.oom = order
                self.fformat = fformat
                matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
            def _set_order_of_magnitude(self):
                self.orderOfMagnitude = self.oom
            def _set_format(self, vmin=None, vmax=None):
                self.format = self.fformat
                if self._useMathText:
                    self.format = r'$\mathdefault{%s}$' % self.format

        ax.yaxis.set_major_formatter(OOMFormatter(4, "%1.1f"))
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0), useMathText=True)
        ax.set_xticklabels([])


    elif (row == 1 and column == 0):
        ax.set_ylabel("Latency (ms)", fontsize=13)
        ax.set_yticks([500, 1000, 1500])
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0), useMathText=True)

        ax.set_xlabel("Number of Nodes", fontsize=13)



    elif (row == 1 and column == 1):
        ax.set_yticks([500, 1000, 1500])
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0), useMathText=True)
        ax.yaxis.get_offset_text().set_position((0,0))


        ax.set_xlabel("Number of Nodes", fontsize=13)


    t = ax.yaxis.get_offset_text()
    t.set_x(-0.13)
    ax.set_xticks([4, 8, 12, 16])


if __name__ == "__main__":
    csv_file1 = "results/pnc_max_tp_scale.csv"
    csv_file3 = "results/pnc_max_lt_scale.csv"
    csv_file2 = "results/orset_max_tp_scale.csv"
    csv_file4 = "results/orset_max_lt_scale.csv"
    
    fig_file_name = "results/scale.pdf"

    fig, axs  = plt.subplots(2, 2, figsize=(8.3, 4.5))
    plt.subplots_adjust(wspace=10, hspace=10)


    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rc('figure', titlesize=20)  # fontsize of the figure title

    plot_lines(csv_file1, axs[0][0], 0, 0)
    plot_lines(csv_file2, axs[0][1], 0, 1)
    plot_lines(csv_file3, axs[1][0], 1, 0)
    plot_lines(csv_file4, axs[1][1], 1, 1)
    

    plt.subplots_adjust(wspace=0.15, hspace=0.1)
    fig.savefig(fig_file_name, dpi=300, format="pdf", bbox_inches="tight")
