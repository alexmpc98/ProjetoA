import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d 

EjetLatitude = 32.61
EjetLongitude = -16.71
DeclinacaoSol = {}

#ALINEA A

dados = np.loadtxt("AG1.txt", skiprows=1)
ano = dados[:,0].astype(int)
mes = dados[:,1].astype(int)
dia = dados[:,2].astype(int)
hora = dados[:,3].astype(int)
t2 = dados[:,4] #temperatura do ar
swdown = dados[:,5] #radiação solar descrescente
lwdown = dados[:,6] #radiação atmosférica decrescente
u10 = dados[:,7] #vento de componente u
v10 = dados[:,8] #vento de componente v

#ALINEA B

datas = []
for h in range(len(ano)):
    datas.append(datetime.datetime(ano[h], mes[h], dia[h], hora[h]))

datas_A= np.array(datas)


w = (hora - 12) * (360/24) + EjetLongitude

julians = np.zeros(ano.shape)
for h in range(len(julians)):
    ano0 = datas[h].year
    julians[h] = datas[h].toordinal()-datetime.datetime(ano0-1, 12, 31).toordinal()

CalculoSinDecSol = -0.39779 * np.cos(0.98565 * (julians[h]+10)+1.914*np.sin(0.98565 * (julians[h]-2)))

AngulosDeclinacaoSol=np.arcsin(CalculoSinDecSol)

CalculoCosAngZen = np.sin(EjetLatitude) * np.sin(AngulosDeclinacaoSol) + np.cos(EjetLatitude) * np.cos(AngulosDeclinacaoSol) * np.cos(w)

CalcAngZen = np.arccos(CalculoCosAngZen)



#ALINEA C

def interpl(y0):
    y = np.copy(y0)
    x = np.arange(len(t2)) 
    x1 = x[np.where(y != -999)]
    y1 = y[np.where(y != -999)]
    f = interp1d(x1, y1, kind = "linear", fill_value = "extrapolate")
    x1 = np.where(y == -999)
    return y

t2_interp = interpl(t2)
swdown_interp = interpl(swdown)
u10_interp = interpl(u10)
v10_interp = interpl(v10)



#ALINEA D

temperatura_celcius = t2 - 273.15                                                    ###converter as temperaturas a celcius
temperatura_corrigida = np.where(temperatura_celcius == -1272.15, 0, temperatura_celcius)     ###substituir os -1272.12(=-999-273.15) por zero


th = []
for h in range(24):
    indexs = np.argwhere((mes == 1) & (hora == h))         ###cria uma lista (th) com media das temperaturas hora a hora nos meses 7
    th.append(np.mean(temperatura_corrigida[indexs]))


xvalores = range(24)                                       ###constroi o gráfico
yvalores = th
plt.plot(xvalores, yvalores, '-o')
plt.xlabel("hora do dia")
plt.ylabel("temperatura media em Celcius")
plt.show()





