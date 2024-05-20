import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('C:\\Users\\cmcke\\OneDrive\\Desktop\\COS\\personal\\EarthClimateModel_VS\\earthmodel.xlsx', sheet_name='Model')

data = {
    'x': [1,2,3],
    'y': [3,4,5],
    'val': [10,20,30]
}
df = pd.DataFrame(data)

plt.figure(figsize=(10,6))
sc = plt.scatter(df['x'], df['y'], c=df['val'], cmap='viridis', s=100)

plt.colorbar(sc, labels='val')

plt.xlabel('Xax')
plt.ylabel('Yax')

plt.show()