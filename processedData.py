import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from seaborn.matrix import heatmap

from cleanedData import df as cleanedData

# compose :: (f, g) -> x -> g(f(x))
compose = lambda f, g: lambda x: g(f(x))
# averageColumn :: list -> float
averageList = lambda inputList: sum(inputList) / len(inputList)

# removePercentAndConvertColumnToList :: column -> list
removePercentAndConvertColumnToList = lambda inputColumn: list(
    map(lambda i: float(i.strip("%")), inputColumn.tolist())
)

# averageOfFixedColumn :: column -> float
averageOfFixedColumn = compose(removePercentAndConvertColumnToList, averageList)

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

# Correlation Plot
# correlationHeatmap("kendall")
# plt.savefig("kendall.png", bbox_inches="tight")
# correlationHeatmap("spearman")
# plt.savefig("spearman.png", bbox_inches="tight")

# Bar Plot
uninsuredRate2010 = dfCleanedData["Uninsured Rate (2010)"]
uninsuredRate2015 = dfCleanedData["Uninsured Rate (2015)"]

bars = {
    2010: averageOfFixedColumn(uninsuredRate2010),
    2015: averageOfFixedColumn(uninsuredRate2015),
}
print(bars)

sns.barplot(data=bars)
plt.xlabel("Year")
plt.ylabel("Percentage of Population Uninsured")
plt.savefig("barGraph.png", bbox_inches="tight")
plt.show()
