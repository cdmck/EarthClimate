import pandas as pd
import matplotlib.pyplot as plt
import math

df = pd.read_excel('C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\EarthClimateModel_VS\\earthmodel.xlsx', sheet_name='Model', header=3)

# command line arguments
mu # fraction of emissions avoided
Xmax # cost of most expensive carbon emission reduction tech
pureTimePrefFactor
ineqAverFactor

tempColumn = df['Earth Temp (C)']
earthTemp = tempColumn.to_numpy()

year = 2024
popGrowthRate = 1.5 - 1.5 * (year - 1990) / 80 # % per year
globalPop = 8.1 # 10^9 people
deltaT = earthTemp - earthTemp[1] # current minus pre-industrial
prodGrowthRate = (popGrowthRate + 2.2 - (2.2-0.33) * (year - 2000) / 1000) - 0.001 * deltaT ^2  # % per year
globalProd = 90000 # 10^9 $ per year
carbonIntensity = 0.000222 * math.e(-0.015 * (year - 1980)) # tons of carbon emitted per $ globalProd
carbonEmissions = carbonIntensity * globalProd * (1 - mu) # 10^12 ton carbon per year
damageFunction = 1/(1 + 0.0018 * deltaT + 0.0023 * (deltaT)^2) * 0.97436
averageCarbonCost = (mu * Xmax) / 2 # $ per ton of carbon abated
co2frac = carbonIntensity * mu * averageCarbonCost # fraction of globalProd spent on CO2 emission reductions
consumPerCap = (globalProd / globalPop) * damageFunction * (1 - co2frac) # 1990 US $ per person per year
timePref = 1 / ((1 + pureTimePrefFactor)^(year - 2024)) # relative importance of each year
utility = (((consumPerCap^(1 - ineqAverFactor) / (1 - ineqAverFactor))) - (9000^(1 - ineqAverFactor) / (1 - ineqAverFactor))) # per capita welfare relative to a per capita income of $9000/yr
socialWelfare = timePref * globalPop * utility

SCC


for value in earthTemp[224:]:
    # sum the socialWelfare for each year from 2024 to 4000 
    # to calculate the social cost of carbon

    SCC += socialWelfare
    
print(SCC)
