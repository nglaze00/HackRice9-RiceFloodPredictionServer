import numpy as np
import sklearn.ensemble
import utils
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
        precip = np.loadtxt("precip_train.txt")
        depths = np.loadtxt("depths_train.txt")

        self.thresholds = []
        self.train(depths, precip)

    def get_thresholds(self):
        return self.thresholds


    def train(self, depths, precip):
        """
        Trains the model.
        :param depths:
        :param precip:
        :return:
        """
        for node in range(len(depths[0])):
            
            flood_levels = []


            for date in range(len(depths)):


                if depths[date][node] >= utils.FLOODED_THRESHOLD:

                    flood_levels.append(precip[date])



            self.thresholds.append(np.mean(flood_levels))


    def fit(self, precip_today):
        """
        Given an amount of rain (in inches), return a list where flooded[i] is whether node i will be flooded
        :return:
        """
        return [precip_today >= self.thresholds[i] for i in range(len(self.thresholds))]

m = LinearRainModel()
print(m.thresholds)