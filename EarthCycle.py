import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
from decimal import Decimal, getcontext

getcontext().prec = 20

df = pd.read_excel('C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\EarthClimateModel_VS\\earthmodel.xlsx', sheet_name='Model', header=3)

parser = argparse.ArgumentParser(description='Calculate the SCC')
parser.add_argument('mu', type=float, help='Fraction of emissions avoided')
parser.add_argument('Xmax', type=float, help='Cost of the most expensive carbon emission reduction technology')
parser.add_argument('pureTimePrefFactor', type=float, help='Pure time preference factor')
parser.add_argument('ineqAverFactor', type=float, help='Inequality aversion factor')
args = parser.parse_args()

# Command line arguments
mu = Decimal(args.mu)  # Convert to Decimal
Xmax = Decimal(args.Xmax)  # Convert to Decimal
pureTimePrefFactor = Decimal(args.pureTimePrefFactor)  # Convert to Decimal
ineqAverFactor = Decimal(args.ineqAverFactor)  # Convert to Decimal

tempColumn = df['Earth Temp (C)']
earthTemp = [Decimal(temp) for temp in tempColumn.to_numpy()]

yearInit = 2024
popInit = Decimal('8.1')
globalProdInit = Decimal('90000')
carbonIntensityInit = Decimal('0.000222') * Decimal(np.exp(-0.015 * (yearInit - 1980)))

SCC = Decimal('0')

# Calculate deltaT
deltaT = (earthTemp[224] - earthTemp[0]) * Decimal('1.05')

# Calculate population growth rate (CI)
popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(yearInit - 1990) / Decimal('80')

# Calculate production growth rate (CK)
prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(yearInit - 2000) / Decimal('1000')) - Decimal('0.001') * deltaT ** 2

# Calculate carbon intensity (CM)
carbonIntensity = carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(yearInit - yearInit)

# Calculate carbon emissions (CN)
# carbonEmissions = carbonIntensity * globalProdInit * (Decimal('1') - mu)

# Calculate damage function (CQ)
damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2)))) * Decimal('0.97436')
print("delatT = ", deltaT)

# Calculate average carbon cost (CS)
averageCarbonCost = (mu * Xmax) / Decimal('2')

# Calculate CO2 fraction (CT)
co2frac = carbonIntensity * mu * averageCarbonCost

# Calculate consumption per capita (CU)
consumPerCap = (globalProdInit / popInit) * damageFunction * (Decimal('1') - co2frac)
print("globalProdinit = ", globalProdInit)
print("popInit", popInit)
print("damagefun = ", damageFunction)
print("co2frac = ", co2frac)
print("consumtion = ", consumPerCap)

# Calculate time preference (CV)
timePref = Decimal('1') / ((Decimal('1') + pureTimePrefFactor) ** Decimal(yearInit - yearInit))

# Calculate utility (CW)
utility = (((consumPerCap ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor))) - (Decimal('9000') ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor)))
print("utility intial = ", utility)

# Calculate social welfare (CX)
socialWelfare = timePref * popInit * utility
print("socialWelfare initial = ", socialWelfare)

# Sum the social welfare to get SCC
SCC += socialWelfare

# For subsequent iterations, set mu, averageCarbonCost, and co2frac to 0
mu = Decimal('0')
averageCarbonCost = Decimal('0')
co2frac = Decimal('0')
globalPop = popInit
globalProd = globalProdInit

for i, temp in enumerate(earthTemp[225:4000:]):
    # Sum the socialWelfare for each year from 2024 to 4000 
    # to calculate the social cost of carbon

    year = yearInit + i

    # Calculate deltaT
    deltaT = (temp - earthTemp[0]) * Decimal('1.05')

    # Calculate population growth rate (CI)
    popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(year - 1990) / Decimal('80')

    # Calculate global population (CJ)
    globalPop *= (Decimal('1') + popGrowthRate / Decimal('100'))

    # Calculate production growth rate (CK)
    prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(year - 2000) / Decimal('1000')) - (Decimal('0.001') * deltaT ** 2)

    # Calculate global production (CL)
    globalProd = globalProd * (Decimal('1') + prodGrowthRate / Decimal('100'))

    # Calculate carbon intensity (CM)
    carbonIntensity = carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(year - yearInit)

    # Calculate carbon emissions (CN)
    # carbonEmissions = carbonIntensity * globalProd * (Decimal('1') - mu)

    # Calculate damage function (CQ)
    damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2)))) * Decimal('0.97436')

    # Calculate average carbon cost (CS)
    averageCarbonCost = (mu * Xmax) / Decimal('2')

    # Calculate CO2 fraction (CT)
    co2frac = carbonIntensity * mu * averageCarbonCost

    # Calculate consumption per capita (CU)
    consumPerCap = (globalProd / globalPop) * damageFunction
    # print("consumPerCAp = ", consumPerCap)
    # print("globalProd = ", globalProd)
    # print("globalPop  = ", globalPop)
    # print("damageFunction = ", damageFunction)

    # Calculate time preference (CV)
    timePref = Decimal('1') / ((Decimal('1') + pureTimePrefFactor) ** Decimal(year - yearInit + 1))

    # Calculate utility (CW)
    utility = (((consumPerCap ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor))) - (Decimal('9000') ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor)))

    # Calculate social welfare (CX)
    print("utility = ", utility)
    print("globalPop = ", globalPop)
    print("timePref = ", timePref)
    socialWelfare = timePref * globalPop * utility

    # Sum the social welfare to get SCC
    SCC += socialWelfare
    print("welfare = ", socialWelfare)

print(SCC)