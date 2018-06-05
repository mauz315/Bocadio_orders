
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

from pandas import DataFrame

df = pd.read_csv('orders_distrito.csv')
df.fecha = pd.to_datetime(df.fecha)
# df.reset_index(drop=True, inplace=True)
# df.set_index("id_order", inplace=True)
a =[]
for i in df.index:
    if len(df.hora_entrega[i]) == 8:
        df.at[i, 'hora_entrega'] = "Express"

fig = plt.figure
# plt.hist(df, column="distrito")

df['distrito'].value_counts().plot(kind='bar')
# plt.xlabel('Distrito')
# plt.ylabel('Pedidos')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.savefig('graph1.png')
plt.show()

fig2 = plt.figure
df['hora_entrega'].value_counts().plot(kind='bar')
# plt.xlabel('Distrito')
# plt.ylabel('Pedidos')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.savefig('graph2.png')
plt.show()

# fig3 = plt.figure
# df.hist(column="hora_pedido")
# plt.grid(True)
# plt.savefig('graph3.png')
# plt.show()