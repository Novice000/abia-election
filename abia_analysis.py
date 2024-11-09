import pandas as pd
import numpy as np
from geopy.distance import geodesic
from scipy.spatial import cKDTree
from statistics import stdev, mean


# Load the data
data = pd.read_csv("abia_data.csv")
data["PU-Name"] = data["PU-Name"].apply(str.strip)
# Initialize the cluster dictionary
cluster = {}

# Extract coordinates
coordinates = data[['lat', 'long']].to_numpy()

# Create a KDTree for efficient spatial queries
tree = cKDTree(np.radians(coordinates))

# Define the radius (6 km converted to radians)
radius = 6 / 6371.0  # Approximate radius of Earth in kilometers

# Iterate over each point in the data
for idx, (x_name, x_cor) in enumerate(zip(data['PU-Name'], coordinates)):
    x_name = str(x_name).strip()
    
    # Query the KDTree for neighbors within the radius
    indices = tree.query_ball_point(np.radians(x_cor), radius)
    
    cluster[x_name] = []
    
    for neighbor_idx in indices:
        y_name = str(data.loc[neighbor_idx, 'PU-Name'])
        y_cor = (data.loc[neighbor_idx, 'lat'], data.loc[neighbor_idx, 'long'])
        
        # Calculate the exact geodesic distance to filter accurately
        distance = geodesic((x_cor[0], x_cor[1]), y_cor).kilometers
        if distance < 6:
            if y_name not in cluster[x_name]:  # Ensure no duplicate entries
                cluster[x_name].append(y_name)

cluster_name = [f"{cluster[name]}" for name in data['PU-Name']]
data["neighbors"] = cluster_name

# Initialize vote clusters
apc_vote_cl = [[] for _ in range(len(data))]
lp_vote_cl = [[] for _ in range(len(data))]
pdp_vote_cl = [[] for _ in range(len(data))]
nnpp_vote_cl = [[] for _ in range(len(data))]

# Populate the vote clusters
for idx, (x_name, pu_names) in enumerate(zip(data['PU-Name'], cluster_name)):
    pu_names = eval(pu_names)  # Convert string representation of list back to list
    for pu in pu_names:
        if pu:
            apc_votes = data.loc[data["PU-Name"] == pu, "APC"]
            lp_votes = data.loc[data["PU-Name"] == pu, "LP"]
            pdp_votes = data.loc[data["PU-Name"] == pu, "PDP"]
            nnpp_votes = data.loc[data["PU-Name"] == pu, "NNPP"]

            apc_vote_cl[idx].append(int(apc_votes.values[0]) if not apc_votes.empty else 0)
            lp_vote_cl[idx].append(int(lp_votes.values[0]) if not lp_votes.empty else 0)
            pdp_vote_cl[idx].append(int(pdp_votes.values[0]) if not pdp_votes.empty else 0)
            nnpp_vote_cl[idx].append(int(nnpp_votes.values[0]) if not nnpp_votes.empty else 0)


#debug votes
print(apc_votes)
print(lp_votes)
print(pdp_votes)
print(nnpp_votes)

# Calculate means and standard deviations
mean_apc = [mean(votes) if votes else 0 for votes in apc_vote_cl]
mean_lp = [mean(votes) if votes else 0 for votes in lp_vote_cl]
mean_pdp = [mean(votes) if votes else 0 for votes in pdp_vote_cl]
mean_nnpp = [mean(votes) if votes else 0 for votes in nnpp_vote_cl]

std_apc = [stdev(votes) if len(votes) > 1 else 0 for votes in apc_vote_cl]
std_lp = [stdev(votes) if len(votes) > 1 else 0 for votes in lp_vote_cl]
std_pdp = [stdev(votes) if len(votes) > 1 else 0 for votes in pdp_vote_cl]
std_nnpp = [stdev(votes) if len(votes) > 1 else 0 for votes in nnpp_vote_cl]

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
z_apc = [(row["APC"] - row["mean_apc"]) / row["stdev_apc"] if row["stdev_apc"] != 0 else 0 for _, row in data.iterrows()]
z_lp = [(row["LP"] - row["mean_lp"]) / row["stdev_lp"] if row["stdev_lp"] != 0 else 0 for _, row in data.iterrows()]
z_pdp = [(row["PDP"] - row["mean_pdp"]) / row["stdev_pdp"] if row["stdev_pdp"] != 0 else 0 for _, row in data.iterrows()]
z_nnpp = [(row["NNPP"] - row["mean_nnpp"]) / row["stdev_nnpp"] if row["stdev_nnpp"] != 0 else 0 for _, row in data.iterrows()]

data["z_apc"] = z_apc
data["z_lp"] = z_lp
data["z_pdp"] = z_pdp
data["z_nnpp"] = z_nnpp

# absolute value for  z-scores
abs_z_apc = data["z_apc"].apply(abs)
abs_z_lp = data["z_lp"].apply(abs)
abs_z_pdp = data["z_pdp"].apply(abs)
abs_z_nnpp = data["z_nnpp"].apply(abs)

# adding absolute values to the dataframe
data["abs_z_nnpp"] = abs_z_nnpp
data["abs_z_pdp"] = abs_z_pdp
data["abs_z_lp"] = abs_z_lp
data["abs_z_apc"] = abs_z_apc

# Save the DataFrame to a CSV file
data.to_csv("worked_abia.csv", index=False)
