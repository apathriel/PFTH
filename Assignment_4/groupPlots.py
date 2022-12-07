"""
    Title: To stack or not to Stack
    Author: Gabriel Høst Andersen
    Date: 15/11/22
"""

import numpy as np
import matplotlib.pyplot as plt

def stackedSeriesPlot(series, format, fileName='stackedplot', seriesStart=0, seriesAmount=9):
    data = np.loadtxt(fname=f'data/{series}.{format}', delimiter=',')

    for i in range(seriesStart, seriesAmount):
        plt.plot(data[i, :])
    else: print(f'The following rows have been printed: {seriesStart} to {seriesAmount}')

    plt.title(f'Effects of anti-inflammatory medicine for {seriesAmount} patients', fontsize=16, pad=15)
    plt.ylabel('Inflammation intensity')
    plt.xlabel('Time (Days)')
    plt.savefig(f'figures/{fileName}.png')
    print(f'Figure has been saved to the figures folder as {fileName}.png')

def subplotSeries(series, format, fileName='subplot', seriesStart=0, seriesAmount=9):
    data = np.loadtxt(fname=f'data/{series}.{format}', delimiter=',')
    fig = plt.figure(figsize=(10, 9.0))
    axes = []

    for i in range(seriesStart, seriesAmount):
        axes.append(fig.add_subplot(3, 3, i + 1))
        axes[i].set_ylabel('Inflammation intensity')
        axes[i].set_xlabel('Time (Days)')
        axes[i].plot(data[i, :])
    else: print(f'The following rows have been printed: {seriesStart} to {seriesAmount}. Vizualized in {seriesAmount} subplots')
    
    fig.suptitle(f'Effects of anti-inflammatory medicine for {seriesAmount} patients', fontsize=16)
    fig.tight_layout()
    plt.savefig(f'figures/{fileName}.png') 
    print(f'Figure has been saved to the figures folder as {fileName}.png')
    plt.close()

def main():
    stackedSeriesPlot(series='series-01', format='csv', fileName='stackedSeriesPlot')
    subplotSeries(series='series-01', format='csv', fileName='subplotSeriesPlot')

if __name__ == '__main__':
    main()
