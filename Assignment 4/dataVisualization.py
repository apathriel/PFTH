import matplotlib.pyplot as plt
import numpy as np

def createPlottingFunction(series, format, file, colorMap='Blues'):
    """
    Docstring temp
    """
    data = np.loadtxt(fname=f'data/{series}.{format}', delimiter=',')
    image = plt.plot(data[[0,59],:], data[:, [0,39]])
    plt.ylabel('Patients')
    plt.xlabel('Time')
    plt.savefig(f'figures/{file}.png')
    return data
    
test = createPlottingFunction(series='series-02', format='csv', file='testArray13')