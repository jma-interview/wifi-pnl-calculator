import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64


def build_plot(data_file):
    img = io.BytesIO()

    fig = plt.figure()
    ax = plt.subplot(111)

    df = pd.read_csv(data_file)
    df.set_index("Date", inplace=True)

    for c in df.columns:
        ax.plot(df.index, df[c], label=f"n={c}")

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=5)
    fig.savefig(img, format='png')
    img.seek(0)
    plot_str = base64.b64encode(img.getvalue()).decode()

    return plot_str

if __name__ == "__main__":
    pass

    file = 'output/roi_output.csv'

    print(build_plot(file))

    # imgdata = base64.b64decode(imgstring)

