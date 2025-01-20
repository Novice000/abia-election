import pandas as pd
import numpy as np
from geopy.distance import geodesic
from scipy.spatial import cKDTree
from pprint import pprint
from statistics import stdev, mean

# Load the data
data = pd.read_csv("abia_data.csv")

print(data.columns)
# Initialize the cluster dictionary
cluster = {}

# Extract coordinates
coordinates = data[['lat', 'long']].to_numpy()
print(coordinates.shape)
print(data["PU-Name"].shape)

cluster = {}

print(data.shape)

for x in data.index:
    x_name = str(data.loc[x, "PU-Name"])
    x_cor = (float(data.loc[x, "lat"]), float(data.loc[x, "long"]))
    for y in data.index:
        y_name = str(data.loc[y, "PU-Name"])
        y_cor = (float(data.loc[y, "lat"]), float(data.loc[y, "long"]))
        
        distance = geodesic(x_cor, y_cor).kilometers
        
        if distance < 6:
            if x_name not in cluster:
                cluster[x_name] = [y_name]
            else:
                cluster[x_name].append(y_name)
    
    if x_name not in cluster:
        cluster[x_name] = [None]
        
cluster_name = []

for name, neighbors in cluster.items():
    cluster_name.append(f"{neighbors}")
    
data["neighbors"] = cluster_name

data.to_csv("abia_clusters.csv", index=False)


apc_vote_cl = []
lp_vote_cl = []
pdp_vote_cl = []
nnpp_vote_cl = []

for cl, pu_names in cluster.items():
    each_apc = []
    each_lp = []
    each_pdp = []
    each_nnpp = []
    print(pu_names)
    for pu in pu_names:
        print(pu)
        if not pu:
            cl_pdp = 0
            cl_apc = 0
            cl_nnpp = 0
            cl_lp = 0
        else:
            cl_pdp = data.loc[str(data["PU-Name"]) == pu, "PDP"] if not data.loc[str(data["PU-Name"]) == pu, "PDP"].empty else 0
            
            print(cl_pdp)
            
            cl_lp = data.loc[str(data["PU-Name"]) == pu, "LP"].values[0] if not data.loc[str(data["PU-Name"]) == pu, "LP"].empty else 0
            
            cl_nnpp = data.loc[str(data["PU-Name"]) == pu, "NNPP"].values[0] if not data.loc[str(data["PU-Name"]) == pu, "NNPP"].empty else 0
            
            cl_apc = data.loc[str(data["PU-Name"]) == pu, "APC"].values[0] if not data.loc[data["PU-Name"] == pu, "APC"].empty else 0
        
        each_apc.append(cl_apc)
        each_lp.append(cl_lp)
        each_pdp.append(cl_pdp)
        each_nnpp.append(cl_nnpp)

    apc_vote_cl.append(each_apc)
    lp_vote_cl.append(each_lp)
    pdp_vote_cl.append(each_pdp)
    nnpp_vote_cl.append(each_nnpp)
    

# Calculate means and standard deviations
mean_apc = []
mean_lp = []
mean_pdp = []
mean_nnpp = []

std_apc = []
std_lp = []
std_pdp = []
std_nnpp = []

for i in range(len(apc_vote_cl)):
    mean_apc.append(mean(apc_vote_cl[i]))
    mean_lp.append(mean(lp_vote_cl[i]))
    mean_pdp.append(mean(pdp_vote_cl[i]))
    mean_nnpp.append(mean(nnpp_vote_cl[i]))
    std_apc.append(stdev(apc_vote_cl[i]))
    std_lp.append(stdev(lp_vote_cl[i]))
    std_pdp.append(stdev(pdp_vote_cl[i]))
    std_nnpp.append(stdev(nnpp_vote_cl[i]))

# Assign mean and standard deviation to DataFrame
data["mean_apc"] = mean_apc
data["mean_lp"] = mean_lp
data["mean_pdp"] = mean_pdp
data["mean_nnpp"] = mean_nnpp
data["stdev_apc"] = std_apc
data["stdev_lp"] = std_lp
data["stdev_pdp"] = std_pdp
data["stdev_nnpp"] = std_nnpp

# Calculate z-scores
z_apc = []
z_lp = []
z_pdp = []
z_nnpp = []

for index, row in data.iterrows():
    z_apc.append((float(row["APC"]) - row["mean_apc"]) / row["stdev_apc"])
    z_lp.append((float(row["LP"]) - row["mean_lp"]) / row["stdev_lp"])
    z_pdp.append((float(row["PDP"]) - row["mean_pdp"]) / row["stdev_pdp"])
    z_nnpp.append((float(row["NNPP"]) - row["mean_nnpp"]) / row["stdev_nnpp"])

data["z_apc"] = z_apc
data["z_lp"] = z_lp
data["z_pdp"] = z_pdp
data["z_nnpp"] = z_nnpp

# Save the DataFrame to a CSV file
data.to_csv("worked_abia.csv", index=False)