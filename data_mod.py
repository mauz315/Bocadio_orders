import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
from pandas import DataFrame

df = pd.read_csv('orders_distrito.csv')
df.fecha = pd.to_datetime(df.fecha)
df = df[df.fecha > pd.to_datetime("15/05/2018")]  # Last3weeks
df = df.reset_index(drop=True)  # Restarting index at 0

# df.set_index("id_order", inplace=True)  # Index by id_order

for i in df.index:
    if len(df.hora_entrega[i]) == 8:
        df.at[i, 'hora_entrega'] = "Express"
    if df.distrito[i][0:3] == "Ate":
        df.at[i, 'distrito'] = "Ate"

# creating weekday filtering
wd = []
for i in df.index:
    wd.append(df.fecha[i].weekday())

df = df.assign(weekDay=pd.Series(wd).values)  # Weekday added


def timefix(horapedido):
    d = dict([("11", "11:00 - 12:00"), ("12", "12:00 - 13:00"),
              ("13", "11:00 - 12:00"), ("14", "14:00 - 13:00"),
              ("15", "15:00 - 16:00"), ("16", "16:00 - 17:00"),
              ("17", "17:00 - 18:00"), ("18", "18:00 - 19:00"),
              ("19", "11:00 - 12:00"), ("20", "20:00 - 21:00"),
              ("21", "21:00 - 22:00"), ("10", "11:00 - 12:00"),
              ("09", "11:00 - 12:00")])
    return d[horapedido[0:2]]


h_e = []
for i in df.index:
    if len(df.hora_entrega[i]) != 7:
        h_e.append(df.hora_entrega[i])
    else:
        h_e.append(timefix(df.hora_pedido[i]))

df = df.assign(hora_entrega2=pd.Series(h_e).values)  # histogram column
# Single weekday analysis
nom = {}


def histoday(dataframe, criterio, day):
    v = dataframe.fecha.nunique()
    ddf = pd.DataFrame(dataframe[criterio].value_counts())
    ddf = ddf/v
    ddf = ddf.assign(percent=ddf/sum(ddf[criterio]))
    globals()['ddf%s_%s' % (day, criterio[0:4])] = ddf
    fig = plt.figure
    ddf[criterio].plot(kind='bar')
    plt.tight_layout()
    plt.ylabel('# de Pedidos')
    plt.title(nom[day])
    ax = plt.gca()
    ax.set_ylim([0, ddf[criterio].max()+5])
    plt.savefig('graph/%s_by_%s.png' % (nom[day][0:3], criterio[0:4]))
    plt.show()


for x in range(0, 7):
    globals()['df%s' % x] = df.loc[df.weekDay == x]
    nom['%s' % x] = calendar.day_name[x]
    histoday(globals()['df%s' % x], 'hora_entrega2', str(x))
    histoday(globals()['df%s' % x], 'distrito', str(x))

# uni = df.fecha.nunique()
byDay = pd.DataFrame(df.groupby('weekDay')['id_order'].count())
dayCount = []
diaNom = []
for i in byDay.index:
    dayCount.append(globals()['df%s' % i]['fecha'].nunique())
    diaNom.append(nom[str(i)])
byDay = byDay.assign(dias=pd.Series(dayCount))
byDay = byDay.assign(prom=byDay.id_order/byDay.dias)
byDay = byDay.assign(dia=pd.Series(diaNom))
fig = plt.figure
byDay.plot('dia', 'prom', kind='bar')
plt.tight_layout()
plt.ylabel('# de Pedidos')
plt.title('Orders by dayWeek')
# ax = plt.gca()
# ax.set_ylim([0, ddf[criterio].max()+5])
plt.savefig('day_orders.png')
plt.show()

