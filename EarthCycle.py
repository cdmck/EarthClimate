import pandas as pd
import matplotlib.pyplot as plt
import math
import argparse

df = pd.read_excel('C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\EarthClimateModel_VS\\earthmodel.xlsx', sheet_name='Model', header=3)

parser = argparse.ArgumentParser(description='Calculate the SCC')
parser.add_argument('mu', type=float, help='Fraction of emissions avoided')
parser.add_argument('Xmax', type=float, help='Cost of the most expensive carbon emission reduction technology')
parser.add_argument('pureTimePrefFactor', type=float, help='Pure time preference factor')
parser.add_argument('ineqAverFactor', type=float, help='Inequality aversion factor')
args = parser.parse_args()

# command line arguments
mu = args.mu # fraction of emissions avoided
Xmax = args.Xmax # cost of most expensive carbon emission reduction tech
pureTimePrefFactor = args.pureTimePrefFactor
ineqAverFactor = args.ineqAverFactor

tempColumn = df['Earth Temp (C)']
earthTemp = tempColumn.to_numpy()

yearInit = 2024
popInit = 8.1
globalProdInit = 90000
carbonIntensityInit = 0.000222 * math.exp(-0.015 * (yearInit - 1980))

SCC = 0

# testing

# for i, temp in enumerate(earthTemp[225:230]):
#     # sum the socialWelfare for each year from 2024 to 4000 
#     # to calculate the social cost of carbon

#     year = yearInit + i
#     print(year)

#     deltaT = (temp - earthTemp[1]) * 1.05 # current minus pre-industrial
#     print(deltaT)

#     popGrowthRate = 1.5 - 1.5 * (year - 1990) / 80 # % per year
#     print(popGrowthRate)

#     globalPop = popInit * (1 + popGrowthRate/100) # 10^9 people
#     print(globalPop)

#     prodGrowthRate = (popGrowthRate + 2.2 - (2.2-0.33) * ((year - 1) - 2000) / 1000) - 0.001 * deltaT ** 2  # % per year
#     print(prodGrowthRate)

#     globalProd = globalProdInit * (1 + prodGrowthRate/100) # 10^9 $ per year
#     print(globalProd)

#     carbonIntensity = carbonIntensityInit * (1 - 0.01833)**(year - 2024) # tons of carbon emitted per $ globalProd
#     print(carbonIntensity)

#     carbonEmissions = carbonIntensity * globalProd * (1 - mu) # 10^12 ton carbon per year
#     print(carbonEmissions)

#     damageFunction = 1/(1 + 0.0018 * deltaT + 0.0023 * (deltaT)**2) * 0.97436
#     print(damageFunction)

#     averageCarbonCost = (mu * Xmax) / 2 # $ per ton of carbon abated
#     print(averageCarbonCost)

#     co2frac = carbonIntensity * mu * averageCarbonCost # fraction of globalProd spent on CO2 emission reductions
#     print(co2frac)

#     consumPerCap = (globalProd / globalPop) * damageFunction * (1 - co2frac) # 1990 US $ per person per year
#     print(consumPerCap)

#     timePref = 1 / ((1 + pureTimePrefFactor) ** (year - 2024)) # relative importance of each year
#     print(timePref)

#     utility = (((consumPerCap ** (1 - ineqAverFactor) / (1 - ineqAverFactor))) - (9000 ** (1 - ineqAverFactor) / (1 - ineqAverFactor))) # per capita welfare relative to a per capita income of $9000/yr
#     print(utility)

#     socialWelfare = timePref * globalPop * utility
#     print(socialWelfare)

#     SCC += socialWelfare
#     print(SCC)

#     popInit = globalPop
#     globalProdInit = globalProd
    
# print(SCC)

for i, temp in enumerate(earthTemp[224:]):
    # sum the socialWelfare for each year from 2024 to 4000 
    # to calculate the social cost of carbon

    year = yearInit + i

    deltaT = (temp - earthTemp[1]) * 1.05 # current minus pre-industrial

    popGrowthRate = 1.5 - 1.5 * (year - 1990) / 80 # % per year

    if i == 0:
        globalPop = popInit
        globalProd = globalProdInit
    else:
        globalPop *= (1 + popGrowthRate/100) # 10^9 people
        globalProd *= (1 + prodGrowthRate/100) # 10^9 $ per year

    prodGrowthRate = (popGrowthRate + 2.2 - (2.2-0.33) * ((year - 1) - 2000) / 1000) - 0.001 * deltaT ** 2  # % per year

    carbonIntensity = carbonIntensityInit * (1 - 0.01833)**(year - 2024) # tons of carbon emitted per $ globalProd

    carbonEmissions = carbonIntensity * globalProd * (1 - mu) # 10^12 ton carbon per year

    damageFunction = 1/(1 + 0.0018 * deltaT + 0.0023 * (deltaT)**2) * 0.97436

    averageCarbonCost = (mu * Xmax) / 2 # $ per ton of carbon abated

    co2frac = carbonIntensity * mu * averageCarbonCost # fraction of globalProd spent on CO2 emission reductions

    consumPerCap = (globalProd / globalPop) * damageFunction * (1 - co2frac) # 1990 US $ per person per year

    timePref = 1 / ((1 + pureTimePrefFactor) ** (year - 2024)) # relative importance of each year

    utility = (((consumPerCap ** (1 - ineqAverFactor) / (1 - ineqAverFactor))) - (9000 ** (1 - ineqAverFactor) / (1 - ineqAverFactor))) # per capita welfare relative to a per capita income of $9000/yr

    socialWelfare = timePref * globalPop * utility

    SCC += socialWelfare

    popInit = globalPop
    globalProdInit = globalProd
    
print(SCC)