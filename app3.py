# Create a KDTree for efficient spatial queries
tree = cKDTree(np.radians(coordinates))

# Define the radius (6 km converted to radians)
radius = 6 / 6371.0  # Approximate radius of Earth in kilometers

# Iterate over each point in the data
for idx, (x_name, x_cor) in enumerate(zip(data['PU-Name'], coordinates)):
    x_name = str(x_name).strip()
    
    # Query the KDTree for neighbors within the radius
    indices = tree.query_ball_point(np.radians(x_cor), radius)
    
    for neighbor_idx in indices:
        y_name = str(data.loc[neighbor_idx, 'PU-Name']).strip()
        y_cor = (data.loc[neighbor_idx, 'lat'], data.loc[neighbor_idx, 'long'])
        
        # Calculate the exact geodesic distance to filter accurately
        distance = geodesic((x_cor[0], x_cor[1]), y_cor).kilometers
        if distance < 6:
            if str(x_name) not in cluster:
                cluster[str(x_name)] = []
            if str(y_name) not in cluster[str(x_name)]:  # Ensure no duplicate entries
                cluster[str(x_name)].append(str(y_name))
                
    if str(x_name) not in cluster:
        cluster[str(x_name)] = [None]

