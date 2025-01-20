import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("lagos_2022_train.csv")
print(data.columns)
group = data.groupby(by = "flood")
print(group.head(10))

colour = {"no" : "green",
          "yes": "red"}

fig, ax = plt.subplots(figsize=(6,6))
for k, g in group:
    g.plot(ax=ax, kind="scatter", x = "datetime", y ="precip", label = k, color = colour[k], xlabel= "datetime", ylim= (0,100))
plt.tick_params(labelbottom = False)
plt.show()


for k, g in group:
    g.plot(ax=ax, kind="scatter", x = "datetime", y ="precipcover", label = k, color = colour[k], xlabel= "datetime", ylim= (0,100))
plt.tick_params(labelbottom = False)
plt.show()

weighted = data["precip"].values * (data["precipcover"].values/100)
data["weighted"] = weighted
for k, g in group:
    g.plot(ax=ax, kind="scatter", x = "datetime", y ="weighted", label = k, color = colour[k], ylim= (0,1))
plt.tick_params(labelbottom = False)
plt.show()
