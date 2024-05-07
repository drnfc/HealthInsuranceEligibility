from os import remove

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from seaborn.categorical import barplot
from seaborn.matrix import heatmap

from cleanedData import df as cleanedData
from cleanedData import df_noUS

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
correlationHeatmap("kendall")
plt.savefig("kendall.png", bbox_inches="tight")
plt.show()
correlationHeatmap("spearman")
plt.savefig("spearman.png", bbox_inches="tight")
plt.show()

# Columns
uninsuredRate2010 = dfCleanedData["Uninsured Rate (2010)"]
uninsuredRate2015 = dfCleanedData["Uninsured Rate (2015)"]
medicadeEnrollment2013 = df_noUS["Medicaid Enrollment (2013)"]
medicadeEnrollment2016 = df_noUS["Medicaid Enrollment (2016)"]

bars = {
    2010: averageOfFixedColumn(uninsuredRate2010),
    2015: averageOfFixedColumn(uninsuredRate2015),
}

bars2 = {
    2013: sum(medicadeEnrollment2013),
    2016: sum(medicadeEnrollment2016),
}
barsByState = {
    2010: removePercentAndConvertColumnToList(uninsuredRate2010),
    2015: removePercentAndConvertColumnToList(uninsuredRate2015),
}

barplotDataFramePart1 = pd.DataFrame(
    {
        "State": dfCleanedData["State"],
        2010: removePercentAndConvertColumnToList(uninsuredRate2010),
        2015: removePercentAndConvertColumnToList(uninsuredRate2015),
    }
)

statesBarPlot = pd.melt(
    barplotDataFramePart1, id_vars="State", var_name="Year", value_name="Uninsured Rate"
)

medicateStatesBarplotDataframePart1 = pd.DataFrame(
    {
        "State": df_noUS["State"],
        2013: medicadeEnrollment2013,
        2016: medicadeEnrollment2016,
    }
)
medicadeStatesBarPlot = pd.melt(
    medicateStatesBarplotDataframePart1,
    id_vars="State",
    var_name="Year",
    value_name="Number enrolled in Medicaid (in millions)",
)

print(statesBarPlot)
sns.catplot(
    x="Uninsured Rate",
    y="State",
    hue="Year",
    data=statesBarPlot,
    kind="bar",
    orient="h",
    palette=sns.color_palette(["green", "yellow"]),
)
plt.savefig("BarPlotByStates.png", bbox_inches="tight")
plt.show()

print(statesBarPlot)
sns.catplot(
    x="Number enrolled in Medicaid (in millions)",
    y="State",
    hue="Year",
    data=medicadeStatesBarPlot,
    kind="bar",
    orient="h",
    palette=sns.color_palette(["green", "yellow"]),
)
plt.savefig("MedicaidBarPlotByStates.png", bbox_inches="tight")
plt.show()

sns.barplot(data=bars)
plt.xlabel("Year")
plt.ylabel("Percentage of Population Uninsured (in millions)")
plt.savefig("barGraph.png", bbox_inches="tight")
plt.show()

sns.barplot(data=bars2)
plt.xlabel("Year")
plt.ylabel("Number of Population on Medicaid (in millions)")
plt.savefig("medicadeBarGraph.png", bbox_inches="tight")
plt.show()
