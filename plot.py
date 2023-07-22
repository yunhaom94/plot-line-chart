import pandas as pd
import matplotlib.pyplot as plt


def plot_line_segments(csv_file):
    df = pd.read_csv(csv_file)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # Create a new plot
    plt.figure()

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line Segment Chart')
    for i in range(0, len(df.columns), 2):
        series_x = df.columns[i]
        series_y = df.columns[i+1]
        style = df[series_y].dropna().iloc[-3:].tolist()
        x_cords = df[series_x].dropna().tolist()
        y_cords = df[series_y].dropna().iloc[:-3].tolist()
        x_cords = list(map(float, x_cords))
        y_cords = list(map(float, y_cords))
        print("X:")
        print(x_cords)
        print("Y:")
        print(y_cords)
        print("Style:")
        print(style)
        plt.plot(x_cords, y_cords, label=series_y, linestyle=style[0], marker=style[1], color=style[2])

    # there are more to the loc, placing it outside the chat is more complex
    plt.legend(loc='best')
    plt.grid(True)
    plt.gca().set_xlim(0, 6)
    plt.gca().set_ylim(0, 10)
    plt.show()


if __name__ == "__main__":
    csv_file_path = 'sample.csv'
    plot_line_segments(csv_file_path)
