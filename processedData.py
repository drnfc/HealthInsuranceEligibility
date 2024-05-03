import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from seaborn.matrix import heatmap

from cleanedData import df as cleanedData

# plt configuration
plt.figure(figsize=(16, 6))

# setting up the dataframes
dfCleanedData = pd.DataFrame(cleanedData)

# the methods are found here:
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html
# correlationHeatmap :: method -> corellationHeatmapGraph
correlationHeatmap = lambda coefficient: (
    sns.heatmap(dfCleanedData.corr(numeric_only=True, method=coefficient), annot=True)
).set_title("Correlation Heatmap", fontdict={"fontsize": 12}, pad=12)

correlationHeatmap("kendall")
plt.savefig("kendall.png", bbox_inches="tight")
correlationHeatmap("spearman")
plt.savefig("spearman.png", bbox_inches="tight")
