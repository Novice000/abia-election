from statistics import stdev
from numpy import mean
import pandas as pd
from geopy.distance import geodesic
from pprint import pprint

data = pd.read_csv("abia_data.csv")

cluster = {}

print(data.index)

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

print(len(cluster))
cluster_name = []
                
for cl in cluster:
    cluster_name.append(f"{cluster[cl]}")
    
    
apc_vote_cl = []
lp_vote_cl = []
pdp_vote_cl= []
nnpp_vote_cl = []
cl_vote = []

for cl in cluster:
    each_apc= []
    each_lp= []
    each_pdp= []
    each_nnpp= []
    
    for pu in cl:
        cl_pdp = data[data["PU-Name"] == pu, "PDP"]
        cl_lp = data[data["PU-Name"] == pu, "LP"]
        cl_nnpp = data[data["PU-Name"] == pu, "NNPP"]
        cl_apc = data[data["PU-Name"] == pu, "APC"]
        each_apc.append(cl_apc)
        each_lp.append(cl_lp)
        each_pdp.append(cl_pdp)
        each_nnpp.append(cl_nnpp)

    apc_vote_cl.append(each_apc)
    lp_vote_cl.append(each_lp)
    pdp_vote_cl.append(each_pdp)
    nnpp_vote_cl.append(each_nnpp)
        
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
    
data["stdev_apc"] = std_apc 
data["stdev_lp"] = std_lp 
data["stdev_pdp"] = std_pdp 
data["stdev_nnpp"] = std_nnpp

data["mean_apc"] = mean_apc 
data["mean_lp"] = mean_lp 
data["mean_pdp"] = mean_pdp 
data["mean_nnpp"] = mean_nnpp

z_apc = []
z_lp = []
z_pdp = []
z_nnpp = []

for index, row in data.iterrows():
    z_apc.append((float(row["APC"]) - row["mean_apc"])/row["stdev_apc"])
    z_apc.append((float(row["LP"]) - row["mean_lp"])/row["stdev_lp"])
    z_apc.append((float(row["PDP"]) - row["mean_pdp"])/row["stdevpdp"])
    z_apc.append((float(row["NNPP"]) - row["mean_nnpp"])/row["stdev_nnpp"])
    
data["z_apc"] = z_apc
data["z_lp"] = z_lp
data["z_pdp"] = z_pdp
data["z_nnpp"] = z_nnpp


data.to_csv("worked_abia", index= False)