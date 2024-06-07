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

# Calculate deltaT
deltaT = (earthTemp[224] - earthTemp[0]) * 1.05

# Calculate population growth rate (CI)
popGrowthRate = 1.5 - 1.5 * (yearInit - 1990) / 80

# Calculate production growth rate (CK)
prodGrowthRate = (popGrowthRate + 2.2 - (2.2 - 0.33) * (yearInit - 2000) / 1000) - 0.001 * deltaT ** 2

# Calculate carbon intensity (CM)
carbonIntensity = carbonIntensityInit * (1 - 0.01833) ** (yearInit - yearInit)

# Calculate carbon emissions (CN)
carbonEmissions = carbonIntensity * globalProdInit * (1 - mu)

# Calculate damage function (CQ)
damageFunction = 1 / ((1 + (0.0018 * deltaT) + (0.0023 * (deltaT ** 2))) * 0.97436)

# Calculate average carbon cost (CS)
averageCarbonCost = (mu * Xmax) / 2

# Calculate CO2 fraction (CT)
co2frac = carbonIntensity * mu * averageCarbonCost

# Calculate consumption per capita (CU)
consumPerCap = (globalProdInit / popInit) * damageFunction * (1 - co2frac)

# Calculate time preference (CV)
timePref = 1 / ((1 + pureTimePrefFactor) ** (yearInit - yearInit))

# Calculate utility (CW)
utility = ((consumPerCap ** (1 - ineqAverFactor)) / (1 - ineqAverFactor)) - ((9000 ** (1 - ineqAverFactor)) / (1 - ineqAverFactor))

# Calculate social welfare (CX)
socialWelfare = timePref * popInit * utility

# Sum the social welfare to get SCC
SCC += socialWelfare

# For subsequent iterations, set mu, averageCarbonCost, and co2frac to 0
mu = 0
averageCarbonCost = 0
co2frac = 0
globalPop = popInit
globalProd = globalProdInit

for i, temp in enumerate(earthTemp[225:]):
    # sum the socialWelfare for each year from 2024 to 4000 
    # to calculate the social cost of carbon

    year = yearInit + i

    # Calculate deltaT
    deltaT = (temp - earthTemp[0]) * 1.05

    # Calculate population growth rate (CI)
    popGrowthRate = 1.5 - 1.5 * (year - 1990) / 80

    # Calculate global population (CJ)
    globalPop *= (1 + popGrowthRate / 100)

    # Calculate production growth rate (CK)
    prodGrowthRate = (popGrowthRate + 2.2 - (2.2 - 0.33) * (year - 2000) / 1000) - (0.001 * deltaT ** 2)

    # Calculate global production (CL)
    globalProd *= (1 + prodGrowthRate / 100)

    # Calculate carbon intensity (CM)
    carbonIntensity = carbonIntensityInit * (1 - 0.01833) ** (year - yearInit)

    # Calculate carbon emissions (CN)
    carbonEmissions = carbonIntensity * globalProd * (1 - mu)

    # Calculate damage function (CQ)
    damageFunction = 1 / ((1 + (0.0018 * deltaT) + (0.0023 * (deltaT ** 2))) * 0.97436)

    # Calculate average carbon cost (CS)
    averageCarbonCost = (mu * Xmax) / 2

    # Calculate CO2 fraction (CT)
    co2frac = carbonIntensity * mu * averageCarbonCost

    # Calculate consumption per capita (CU)
    consumPerCap = (globalProd / globalPop) * damageFunction

    # Calculate time preference (CV)
    timePref = 1 / ((1 + pureTimePrefFactor) ** (year - yearInit + 1))

    # Calculate utility (CW)
    utility = ((consumPerCap ** (1 - ineqAverFactor)) / (1 - ineqAverFactor)) - ((9000 ** (1 - ineqAverFactor)) / (1 - ineqAverFactor))

    # Calculate social welfare (CX)
    socialWelfare = timePref * globalPop * utility

    # Sum the social welfare to get SCC
    SCC += socialWelfare

print(SCC)