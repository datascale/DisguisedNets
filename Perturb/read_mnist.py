import os
import struct
import math
import numpy as np
import pandas as pd

"""
Loosely inspired by http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py
which is GPL licensed.
"""
np.set_printoptions(linewidth=160)

def read(dataset = "training", path = "."):
    """
    Python function for importing the MNIST data set.  It returns an iterator
    of 2-tuples with the first element being the label and the second element
    being a numpy.uint8 2D array of pixel data for the given image.
    """

    if dataset is "training":
        fname_img = os.path.join(path, './train-images-idx3-ubyte')
        fname_lbl = os.path.join(path, './train-labels-idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, './t10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, './t10k-labels-idx1-ubyte')
    else:
        raise ValueError, "dataset must be 'testing' or 'training'"

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)

    get_img = lambda idx: (lbl[idx], img[idx])

    # Create an iterator which returns each image in turn
    for i in xrange(len(lbl)):
        yield get_img(i)

def show(image):
    """
    Render a given numpy.uint8 2D array of pixel data.
    """
    from matplotlib import pyplot
    import matplotlib as mpl
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    pyplot.show()

def serialize(data):
    '''
    Converts image to a one dimensional array
    '''
    clean_data=[]
    for e_image in data:
        serial_rows=[]
        for row in e_image[1]:
            serial_rows+=list(row)
        clean_data.append(serial_rows)
    #print clean_data
    return clean_data
	
training_data = list(read("training"))
testing_data = list(read("testing"))

y_train = [training_data[x][0] for x in range(len(training_data))]
y_test = [testing_data[x][0] for x in range(len(testing_data))]

headerc =["pixel"+str(i) for i in range(len(testing_data[0][1])**2)]

training_data = serialize(training_data)
testing_data = serialize(testing_data)


data_train = pd.DataFrame(training_data, columns=headerc)
data_train.insert(0,'label',y_train)
data_train.to_csv('mnist_train.csv',sep=',',index=False)

data_test = pd.DataFrame(testing_data, columns=headerc)
y_test = pd.DataFrame(y_test,columns = ['label'])
data_test.to_csv('mnist_test.csv',sep=',',index=False)
y_test.to_csv('mnist_test_labels.csv',sep=',',index=False)

