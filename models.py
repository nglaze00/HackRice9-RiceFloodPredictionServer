import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

import utils
# TODO change back to XGBoost

XGB_PARAMS =  {
            'eta': 0.3,
            'max_depth': 3,
            'objective': 'multi:softprob',
            'num_class': 2}

XGB_STEPS = 20  # The number of training iterations

class NodeFloodPredictor:
    """
    Model that predicts whether a given node is flooded given the status of all other nodes.
    """
    def __init__(self, target_node):
        """
        Trains an XGBoost model to predict, given the status of all other nodes, whether the target node is flooded.
        :param target_node: node for which predictions will be made
        """
        self.node = target_node
        self.depths_bool = np.loadtxt("depths_train.txt") >= utils.FLOODED_THRESHOLD
        # self.model = xgb.XGBClassifier()
        self.model = RandomForestClassifier(n_estimators=100)
        # Split into train / test data
        self.X_train, self.X_test, self.y_train, self.y_test = self.partition_data(self.depths_bool, 0.995)


    def partition_data(self, depths, ratio):
        """
        Splits water depth data at each node into training & test samples
        :param depths: boolean numpy array, with rows = dates, cols = nodes
        :return: X_train, X_test, y_train, y_test
        """
        y = depths[:, self.node]
        X = np.delete(depths, self.node, axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ratio)
        return X_train, X_test, y_train, y_test

    def train(self):
        """
        Trains the XGBoost classifier on self.X_train, self.y_train
        """
        print("Training XGBoost on node " + str(self.node))
        self.model.fit(self.X_train, self.y_train)

    def predict(self, x):
        """
        Returns the predicted flooding status given status x of other nodes
        """
        return self.model.predict(x)

    def test(self):
        """
        Tests the XGBoost clasifier on self.X_test, self.y_test.
        """
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))

# n = NodeFloodPredictor(14)
# n.train()
# n.test()
class LinearRainModel:
    """
    Model that predicts which nodes will flood given only today's precipitation.
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

           # mean = 0
            #count = 0




            for date in range(len(depths)):


                if depths[date][node] >= 4:

                    flood_levels.append(precip[date])
                   # mean += precip[date]


            self.thresholds.append(np.mean(flood_levels))

        self.thresholds = [thresh * 6 for thresh in self.thresholds]
    def fit(self, precip_today):
        """
        Given an amount of rain (in inches), return a list where flooded[i] is whether node i will be flooded
        :return:
        """
        return [precip_today >= self.thresholds[i] for i in range(len(self.thresholds))]