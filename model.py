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
        self.thresholds = []

    def get_tresholds(self):

        return self.thresholds
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
        for i in range(len(depths)):

            mean = 0

            for j in range(len(precip)):

                if depths[i][j] >= utils.FLOODED_THRESHOLD:

                    mean += depths[i][j]

            mean = float(mean)/len(precip)

            self.thresholds.append(mean)






    def fit(self, precip):
        """
        Given an amount of rain (in inches), return a list where flooded[i] is whether node i will be flooded
        :return:
        """