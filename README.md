# HackRice9-RiceFloodPredictionServer
This is the backend (server) code.

Detailed description: https://devpost.com/software/put-it-in-rice-flood-prediction-navigation-on-rice-s-campus


Frontend (website) code: https://github.com/nglaze00/HackRice9-RiceFloodPredictionWebsite

Server for the "Put it in Rice" project.
Allows user to do the following:
 * Identify which major Rice University campus locations may be flooded via a map and colored icons (waters level given by combined user input or predicted using historical data and current weather conditions)
 * Report flood levels at these locations
 * Predict which locations on campus are flooded, based on today's rain and the reported statuses of other nodes (XGBoost)
 * Generate a dry path from one campus location to another (networkx; Dijkstra's)
This is all accomplished via API connection to a Python Flask server, which stores the data on a Google Cloud-hosted MongoDB cluster.
