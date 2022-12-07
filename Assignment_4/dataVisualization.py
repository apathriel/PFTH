"""
    Title: Custom plotting function
    Author: Gabriel Høst Andersen
    Date: 15/11/22
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['axes.titlepad'] = 15

def createPlottingFunction(series, format, fileName, colorMap='Blues', normScale='linear', title='', xLabel='', yLabel=''):
    """
    This function will take a given series, with a given format, and after visualizing the data input in series, it will save the visualization 
    as a PNG file with a given file name.
    Please check the following url for cmap documentation: https://matplotlib.org/stable/gallery/color/colormap_reference.html
    Please call mpl.scale.get_scale_names() to get availiable scale levels. 
    title, xLabel and yLabel keyword arguments are empty strings by default, please insert you own if you wish in the function call. 
    """
    data = np.loadtxt(fname=f'data/{series}.{format}', delimiter=',')
    plt.imshow(data, cmap=colorMap, norm=normScale)
    plt.title(label = title, pad = mpl.rcParams['axes.titlepad'])
    plt.ylabel(xLabel)
    plt.xlabel(yLabel)
    plt.savefig(f'figures/{fileName}.png') 
    print(f'Figure has been saved to the figures folder as {fileName}.png')

def main():    
    createPlottingFunction(series='series-01', format='csv', fileName='clinicalTrialDataset', colorMap='bone', normScale='linear', title='Effects of anti-inflammatory medicine', xLabel='Patients', yLabel='Time')

if __name__ == '__main__':
    main()