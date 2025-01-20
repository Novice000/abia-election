# from numpy import shape
import pandas as pd

# abia_data = pd.read_csv("polling-units.csv")
# abia_data =  abia_data[abia_data["state_name"] == "ABIA"]

# hng_abia = pd.read_csv("ABIA_crosschecked.csv")

# # hng_abia_name = hng_abia[hng_abia["PU_"]]
# print(hng_abia.shape)
# print(len(abia_data[abia_data["location.latitude"].isna()]))
# abia_data.fillna(0.0000)
# lat= []
# long = []


# print(hng_abia.tail(5))
# print(abia_data.tail(5))


# # Initialize lists for latitudes and longitudes
# lat = []
# long = []

# # Create a dictionary from abia_data for quick lookup
# abia_dict = {}
# for y in abia_data.index:
#     y_name = str(abia_data.loc[y, "name"]).strip().lower()
#     latitude = abia_data.loc[y, "location.latitude"]
#     longitude = abia_data.loc[y, "location.longitude"]
#     abia_dict[y_name] = (latitude, longitude)

# # Loop through hng_abia and find corresponding lat/long from abia_dict
# for x in hng_abia.index:
#     x_name = str(hng_abia.loc[x, "PU-Name"]).strip().lower()
    
#     # Get latitude and longitude from the dictionary if the name exists
#     if x_name in abia_dict:
#         latitude, longitude = abia_dict[x_name]
#         lat.append(float(latitude))
#         long.append(float(longitude))
#     else:
#         lat.append(None)
#         long.append(None)


            
# print(len(lat), len(long))

# hng_abia["lat"] = lat
# hng_abia["long"] = long

# hng_abia.to_csv("efemena_abia_crosschecked.csv")


# data = pd.read_csv("efemena_abia_crosschecked.csv")
# data = data.dropna()
# data2 = pd.read_csv("null_abia.csv")
# data = data.drop(columns=["Unnamed: 0"])
# data2 = data2.drop(columns=["Unnamed: 0", "Unnamed: 0.1", "lat.1", "long.1"])


# abia_data  = pd.concat([data,data2])
# abia_data.to_csv("abia_data.csv", index= False)

data = pd.read_csv("worked_abia.csv")
data[["abs_z_apc","abs_z_lp","abs_z_pdp","abs_z_nnpp"]] = data[["z_apc","z_lp","z_pdp","z_nnpp"]].map(abs)

data = data.sort_values(by="abs_z_nnpp", ascending= False)

data.to_csv("sorted/sorted_abia_nnpp.csv", index = False)