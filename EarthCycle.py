import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal, getcontext

# set the variables for high precision arithmetic
getcontext().prec = 20

# load the earth climate model
df = pd.read_excel('C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\earthmodel.xlsx', sheet_name='Model', header=3)

# Command line arguments
mu = Decimal(input("Enter the fractions of emissions avoided, mu (suggested range 0.01-0.10): "))
Xmax = Decimal(input("Enter the cost of the most expensive carbon emission reduction technology required to fully cut the global carbon emissions, Xmax, in dollars per ton of carbon abated (suggested range 500-2500): "))
pureTimePrefFactor = Decimal(input("Enter the pure time preference factor (suggested range 0.001-0.020): "))
ineqAverFactor = Decimal(input("Enter the inequality aversion factor (suggested range 1.1-1.7): "))

# parse global warming data from the climate model
tempColumn = df['Earth Temp (C)']
earthTemp = [Decimal(temp) for temp in tempColumn.to_numpy()]

# set intiial conditions for the economic model
yearInit = 2024
popInit = Decimal('8.1')
globalProdInit = Decimal('90000')
carbonIntensityInit = Decimal('0.000222') * Decimal(np.exp(-0.015 * (yearInit - 1980)))
SCC = Decimal('0')
emissionsList = []
welfareList = []

# Calculate the change in temperature from pre-industrial times to the current year
deltaT = (earthTemp[224] - earthTemp[0]) * Decimal('1.05')

# Calculate population growth rate in % per year
popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(yearInit - 1990) / Decimal('80')

# Calculate production growth rate in 10^9 USD per year
prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(yearInit - 2000) / Decimal('1000')) - Decimal('0.001') * deltaT ** 2

# Calculate carbon intensity in tons of carbon emitted per dollar globalProd
carbonIntensity = carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(yearInit - yearInit)

# Calculate carbon emissions in 10^12 tons of carbon per year
carbonEmissions = carbonIntensity * globalProdInit * (Decimal('1') - mu)
emissionsList.append(carbonEmissions)

# Calculate damage function
damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2)))) * Decimal('0.97436')

# Calculate average carbon cost of carbon emission abatement in dollars per ton of carbon abated
averageCarbonCost = (mu * Xmax) / Decimal('2')

# Calculate CO2 fraction of globalProd spent on cutting CO2 emissions
co2frac = carbonIntensity * mu * averageCarbonCost

# Calculate consumption per capita in 1990 USD per person per year
consumPerCap = (globalProdInit / popInit) * damageFunction * (Decimal('1') - co2frac)

# Calculate the relative importance of each year
timePref = Decimal('1') / ((Decimal('1') + pureTimePrefFactor) ** Decimal(yearInit - yearInit))

# Calculate utility the per capita welfare relative to a per capita income of 9000 USD per year
utility = (((consumPerCap ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor))) - (Decimal('9000') ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor)))

# Calculate social welfare
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

    # Set the year
    year = yearInit + i

    deltaT = (temp - earthTemp[0]) * Decimal('1.05')

    # Calculate population growth rate
    if year <= 2070:
        popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(year - 1990) / Decimal('80')
    else: popGrowthRate = 0

    # Calculate global population
    if popGrowthRate >= 0:
            globalPop = globalPop * (Decimal('1') + popGrowthRate / Decimal('100'))
    else: globalPop = globalPop

    # Calculate variables for the given year
    prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(year - 2000) / Decimal('1000')) - (Decimal('0.001') * (deltaT ** 2))
    globalProd = globalProd * (Decimal('1') + prodGrowthRate / Decimal('100'))
    carbonIntensity = carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(year - yearInit)
    carbonEmissions = carbonIntensity * globalProd * (Decimal('1') - mu)
    emissionsList.append(carbonEmissions)
    damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2)))) * Decimal('0.97436')
    averageCarbonCost = (mu * Xmax) / Decimal('2')
    co2frac = carbonIntensity * mu * averageCarbonCost

    # Calculate the variables directly influencing the socialWelfare
    consumPerCap = (globalProd / globalPop) * damageFunction
    timePref = Decimal('1') / ((Decimal('1') + pureTimePrefFactor) ** Decimal(year - yearInit + 1))
    utility = (((consumPerCap ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor))) - (Decimal('9000') ** (Decimal('1') - ineqAverFactor) / (Decimal('1') - ineqAverFactor)))

    # Calculate social welfare
    socialWelfare = timePref * globalPop * utility
    welfareList.append(socialWelfare)

    # Sum the social welfare to get SCC
    SCC += socialWelfare

# Print SCC, rounded to the cent
SCC = round(SCC, 2)
print('\n')
print(f"Social Cost of Carbon: {SCC} dollars per ton of carbon dioxide")

# Plot the social welfare and carbon emissions curves
plt.figure(figsize=(7,4))

# Plot the carbon emissions
plt.subplot(2, 1, 1)
plt.plot(range(yearInit, yearInit + len(emissionsList)), emissionsList, '#8B0000', label='Carbon Emissions')
plt.xlabel('Year')
plt.ylabel('Carbon Emissions')
plt.title('Carbon Emissions Over Time')
plt.legend(['10^12 tons of carbon per year'], loc='upper right')
plt.grid(True)

# Plot social welfare
plt.subplot(2, 1, 2)
years = range(yearInit, yearInit + len(welfareList))
plt.plot(range(yearInit, yearInit + len(welfareList)), welfareList, label='Social Welfare')
plt.fill_between(years, welfareList, color='grey', alpha=0.5)
plt.xlabel('Year')
plt.ylabel('Social Welfare')
plt.title('Social Welfare Over Time')
plt.legend([f'Social cost of carbon: {SCC} dollars per ton of CO2'], loc='upper right')
plt.grid(True)

plt.tight_layout()
plt.show()
