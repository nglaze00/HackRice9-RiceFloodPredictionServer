import numpy as np
import sklearn.ensemble

# TODO MACHINE LEARNING W00

class LinearRainModel:
    """
    Model that predicts the
    """
    def __init__(self):
        """
        Trains a linear model using the data stored in depths_train.txt and precip_train.txt.
        """
        precip = np.loadtxt("precip_train.txt")
        depths = np.loadtxt("depths_train.txt")

        self.thresholds = []
        self.train(depths, precip)


    def train(self, depths, precip):
        """
        Trains the model.
        :param depths:
        :param precip:
        :return:
        """


    def fit(self, precip):
        """
        Given an amount of rain (in inches), return a list where flooded[i] is whether node i will be flooded
        :return:
        """
        return [precip >= self.thresholds[i] for i in range(len(self.thresholds))]