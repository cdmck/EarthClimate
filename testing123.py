import pandas as pd
import numpy as np
from decimal import Decimal, getcontext

class EarthClimateModel:
    def __init__(self, excel_file, mu, Xmax, pureTimePrefFactor, ineqAverFactor):
        self.mu = Decimal(mu)
        self.Xmax = Decimal(Xmax)
        self.pureTimePrefFactor = Decimal(pureTimePrefFactor)
        self.ineqAverFactor = Decimal(ineqAverFactor)
        self.yearInit = 2024
        self.popInit = Decimal('8.1')
        self.globalProdInit = Decimal('90000')
        self.carbonIntensityInit = Decimal('0.000222') * Decimal(np.exp(-0.015 * (self.yearInit - 1980)))
        self.SCC = Decimal('0')
        
        # Load the Excel data
        self.df = pd.read_excel(excel_file, sheet_name='Model', header=3)
        self.earthTemp = [Decimal(temp) for temp in self.df['Earth Temp (C)'].to_numpy()]
        
        # Set the precision
        getcontext().prec = 20
        
    def calculate_scc(self):
        deltaT = (self.earthTemp[224] - self.earthTemp[0]) * Decimal('1.05')
        popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(self.yearInit - 1990) / Decimal('80')
        prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(self.yearInit - 2000) / Decimal('1000')) - Decimal('0.001') * deltaT ** 2
        carbonIntensity = self.carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(self.yearInit - self.yearInit)
        carbonEmissions = carbonIntensity * self.globalProdInit * (Decimal('1') - self.mu)
        damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2))) * Decimal('0.97436'))
        averageCarbonCost = (self.mu * self.Xmax) / Decimal('2')
        co2frac = carbonIntensity * self.mu * averageCarbonCost
        consumPerCap = (self.globalProdInit / self.popInit) * damageFunction * (Decimal('1') - co2frac)
        timePref = Decimal('1') / ((Decimal('1') + self.pureTimePrefFactor) ** Decimal(self.yearInit - self.yearInit))
        utility = ((consumPerCap ** (Decimal('1') - self.ineqAverFactor)) / (Decimal('1') - self.ineqAverFactor)) - ((Decimal('9000') ** (Decimal('1') - self.ineqAverFactor)) / (Decimal('1') - self.ineqAverFactor))
        socialWelfare = timePref * self.popInit * utility
        self.SCC += socialWelfare

        # For subsequent iterations, set mu, averageCarbonCost, and co2frac to 0
        self.mu = Decimal('0')
        averageCarbonCost = Decimal('0')
        co2frac = Decimal('0')
        globalPop = self.popInit
        globalProd = self.globalProdInit

        for i, temp in enumerate(self.earthTemp[225:]):
            year = self.yearInit + i
            deltaT = (temp - self.earthTemp[0]) * Decimal('1.05')
            popGrowthRate = Decimal('1.5') - Decimal('1.5') * Decimal(year - 1990) / Decimal('80')
            globalPop *= (Decimal('1') + popGrowthRate / Decimal('100'))
            prodGrowthRate = (popGrowthRate + Decimal('2.2') - (Decimal('2.2') - Decimal('0.33')) * Decimal(year - 2000) / Decimal('1000')) - (Decimal('0.001') * deltaT ** 2)
            globalProd *= (Decimal('1') + prodGrowthRate / Decimal('100'))
            carbonIntensity = self.carbonIntensityInit * (Decimal('1') - Decimal('0.01833')) ** Decimal(year - self.yearInit)
            carbonEmissions = carbonIntensity * globalProd * (Decimal('1') - self.mu)
            damageFunction = Decimal('1') / ((Decimal('1') + (Decimal('0.0018') * deltaT) + (Decimal('0.0023') * (deltaT ** 2))) * Decimal('0.97436'))
            averageCarbonCost = (self.mu * self.Xmax) / Decimal('2')
            co2frac = carbonIntensity * self.mu * averageCarbonCost
            consumPerCap = (globalProd / globalPop) * damageFunction
            timePref = Decimal('1') / ((Decimal('1') + self.pureTimePrefFactor) ** Decimal(year - self.yearInit + 1))
            utility = ((consumPerCap ** (Decimal('1') - self.ineqAverFactor)) / (Decimal('1') - self.ineqAverFactor)) - ((Decimal('9000') ** (Decimal('1') - self.ineqAverFactor)) / (Decimal('1') - self.ineqAverFactor))
            socialWelfare = timePref * globalPop * utility
            self.SCC += socialWelfare

        return self.SCC

# Usage
excel_file = 'C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\EarthClimateModel_VS\\earthmodel.xlsx'
mu = 0.07
Xmax = 1500
pureTimePrefFactor = 0.005
ineqAverFactor = 1.5

model = EarthClimateModel(excel_file, mu, Xmax, pureTimePrefFactor, ineqAverFactor)
scc_value = model.calculate_scc()
print(f"Calculated SCC: {scc_value}")
