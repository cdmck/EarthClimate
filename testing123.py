import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
from decimal import Decimal, getcontext

getcontext().prec = 20

df = pd.read_excel('C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\EarthClimateModel_VS\\earthmodel.xlsx', sheet_name='Model', header=3)

# Command line arguments
mu = Decimal(input("mu")) # Convert to Decimal
Xmax = Decimal(input("xmax")) # Convert to Decimal
pureTimePrefFactor = Decimal(input("puretimepreffactor")) # Convert to Decimal
ineqAverFactor = Decimal(input("ineqAverFactor"))  # Convert to Decimal

tempColumn = df['Earth Temp (C)']
earthTemp = [Decimal(temp) for temp in tempColumn.to_numpy()]

yearInit = 2024
popInit = Decimal('8.1')
globalProdInit = Decimal('90000')
carbonIntensityInit = Decimal('0.000222') * Decimal(np.exp(-0.015 * (yearInit - 1980)))

SCC = Decimal('0')
emissionsList = []
welfareList = []

# Calculate deltaT
deltaT = (earthTemp[224] - earthTemp[0]) * Decimal('1.05')

# Calculate population growth rate (CI)
popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(yearInit - 1990) / Decimal('80')

# Calculate production growth rate (CK)
prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(yearInit - 2000) / Decimal('1000')) - Decimal('0.001') * deltaT ** 2

# Calculate carbon intensity (CM)
carbonIntensity = carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(yearInit - yearInit)

# Calculate carbon emissions (CN)
carbonEmissions = carbonIntensity * globalProdInit * (Decimal('1') - mu)
emissionsList.append(carbonEmissions)

# Calculate damage function (CQ)
damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2)))) * Decimal('0.97436')

# Calculate average carbon cost (CS)
averageCarbonCost = (mu * Xmax) / Decimal('2')

# Calculate CO2 fraction (CT)
co2frac = carbonIntensity * mu * averageCarbonCost

# Calculate consumption per capita (CU)
consumPerCap = (globalProdInit / popInit) * damageFunction * (Decimal('1') - co2frac)

# Calculate time preference (CV)
timePref = Decimal('1') / ((Decimal('1') + pureTimePrefFactor) ** Decimal(yearInit - yearInit))

# Calculate utility (CW)
utility = (((consumPerCap ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor))) - (Decimal('9000') ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor)))

# Calculate social welfare (CX)
socialWelfare = timePref * popInit * utility
welfareList.append(socialWelfare)

# Sum the social welfare to get SCC
SCC += socialWelfare

# For subsequent iterations, set mu, averageCarbonCost, and co2frac to 0
mu = Decimal('0')
averageCarbonCost = Decimal('0')
co2frac = Decimal('0')
globalPop = popInit
globalProd = globalProdInit

for i, temp in enumerate(earthTemp[225:2201:]):
    # Sum the socialWelfare for each year from 2024 to 4000 
    # to calculate the social cost of carbon

    year = yearInit + i

    # Calculate deltaT
    deltaT = (temp - earthTemp[0]) * Decimal('1.05')

    # Calculate population growth rate (CI)
    if year <= 2070:
        popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(year - 1990) / Decimal('80')
    else: popGrowthRate = 0

    # Calculate global population (CJ)
    if popGrowthRate >= 0:
            globalPop = globalPop * (Decimal('1') + popGrowthRate / Decimal('100'))
    else: globalPop = globalPop

    # Calculate production growth rate (CK)
    prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(year - 2000) / Decimal('1000')) - (Decimal('0.001') * (deltaT ** 2))

    # Calculate global production (CL)
    globalProd = globalProd * (Decimal('1') + prodGrowthRate / Decimal('100'))

    # Calculate carbon intensity (CM)
    carbonIntensity = carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(year - yearInit)

    # calculate carbon emissions (CN)
    carbonEmissions = carbonIntensity * globalProd * (Decimal('1') - mu)
    emissionsList.append(carbonEmissions)

    # Calculate damage function (CQ)
    damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2)))) * Decimal('0.97436')

    # Calculate average carbon cost (CS)
    averageCarbonCost = (mu * Xmax) / Decimal('2')

    # Calculate CO2 fraction (CT)
    co2frac = carbonIntensity * mu * averageCarbonCost

    # Calculate consumption per capita (CU)
    consumPerCap = (globalProd / globalPop) * damageFunction
    
    # Calculate time preference (CV)
    timePref = Decimal('1') / ((Decimal('1') + pureTimePrefFactor) ** Decimal(year - yearInit + 1))

    # Calculate utility (CW)
    utility = (((consumPerCap ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor))) - (Decimal('9000') ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor)))

    # Calculate social welfare (CX)
    socialWelfare = timePref * globalPop * utility
    welfareList.append(socialWelfare)

    # Sum the social welfare to get SCC
    SCC += socialWelfare

print(SCC)

# Plot carbon emissions
plt.figure(figsize=(12, 6))
plt.plot(range(yearInit, yearInit + len(emissionsList)), emissionsList, label='Carbon Emissions')
plt.xlabel('Year')
plt.ylabel('Carbon Emissions')
plt.title('Carbon Emissions Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot social welfare
plt.figure(figsize=(12, 6))
plt.plot(range(yearInit, yearInit + len(welfareList)), welfareList, label='Social Welfare')
plt.xlabel('Year')
plt.ylabel('Social Welfare')
plt.title('Social Welfare Over Time')
plt.legend()
plt.grid(True)
plt.show()