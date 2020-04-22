import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d 

EjetLatitude = 32.61
EjetLongitude = -16.71

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

def diajuliano(ano,mes,dia):
    dia_juliano=datetime.datetime(ano,mes,dia)
    dia_j=dia_juliano.timetuple()
    return dia_j.tm_yday



def zenital(ano,mes,dia,hora):  
    n = diajuliano(ano,mes,dia)
    CalculoSinDecSol = -0.39779 * np.cos(0.98565*np.pi/180 * (n+10)+1.914*np.sin(0.98565*np.pi/180 * (n-2)))
    AngulosDeclinacaoSol=np.arcsin(CalculoSinDecSol)
    w = (hora - 12) * (360/24) + EjetLongitude
    CalculoCosAngZen = np.sin(EjetLatitude*np.pi/180) * np.sin(AngulosDeclinacaoSol) + np.cos(EjetLatitude*np.pi/180) * np.cos(AngulosDeclinacaoSol) * np.cos(w*np.pi/180)
    CalcAngZen = np.arccos(CalculoCosAngZen)
    return(CalcAngZen*180/np.pi)
    

#ALINEA C

def interpl(y0):
    y = np.copy(y0)
    x = np.arange(len(y0)) 
    x1 = x[np.where(y != -999)]
    y1 = y[np.where(y != -999)]
    f = interp1d(x1, y1, kind = "linear", fill_value = "extrapolate")
    x2 = np.where(y == -999)
    y[x2]=f(x[x2])
    return y

t2_interp = interpl(t2)
swdown_interp = interpl(swdown)
u10_interp = interpl(u10)
v10_interp = interpl(v10)



#ALINEA D
 

temperatura_celcius = t2 - 273.15                                                    #converter temperaturas para celcius
temperatura_corrigida = np.where(temperatura_celcius == -1272.15, 0, temperatura_celcius)     #substituir os -1272.12(=-999-273.15) por zero


t = []
for h in range(24):
    indexs = np.argwhere((mes == 1) & (hora == h))         #cria uma lista (t) com media das temperaturas hora a hora nos meses 1
    t.append(np.mean(temperatura_corrigida[indexs]))
        

x = range(24)                                       
y = t
fig , ax= plt.subplots()
plt.plot(x, y, '-o')
ax.set_xlabel("hora do dia")
ax.set_ylabel("temperatura media em Celcius")



#ALINEA E

N=np.arange(1,366)
def declina(N):
    delta=np.arcsin(-0.39779*np.cos(0.98565*np.pi/180*(N+10))+1.914*np.pi/180*np.sin(0.98565*np.pi/180*(N-2)))
    return delta


lat=32.61*np.pi/180
w=np.arccos(-np.tan(lat)*np.tan(declina(15)))/np.pi*12
nascer_do_sol = 12-w     #hora solar
por_do_sol = 12+w        #hora solar



index_ns = np.argwhere((mes == 1) & (hora == round(nascer_do_sol)))        
ns = np.mean(temperatura_corrigida[index_ns])
plt.scatter(nascer_do_sol, round(ns,2), color = "green", marker = "x", s = 500)


index_ps = np.argwhere((mes == 1) & (hora == round(por_do_sol)))         
ps = np.mean(temperatura_corrigida[index_ps])
plt.scatter(por_do_sol, round(ps,2), color = "green", marker = "x", s = 500)


#ALINEA F

rs_media=[]
for h in range(24):
    rs_h=np.argwhere((mes==1) & (hora==h))
    rs_media.append(np.mean(swdown_interp[rs_h])) 

ax1= ax.twinx()
ax1.set_ylabel('Radiação solar')
ax1.plot(rs_media, color='purple')
fig.tight_layout()

#ALINEA G

ang_zen_hora=[]
for h in range(24):
    for a in range(1979,2019):
        for d in range(1,32):
            ang_zen_hora.append([zenital(a,1,d,h)])
            
            
total_de_dias = 31*40                    #31*40 pois existem 31 dias por cada ano, logo 40 anos * 31 dias    
ang_zen_medio=[]
for i in range(0,len(ang_zen_hora),total_de_dias):                      
    ang_zen_medio.append([np.mean(ang_zen_hora[i:i+total_de_dias]),])
    
t_atm=[]
for h in range(24):
    t_atm_h = np.squeeze(np.argwhere((mes == 1) & (hora == h)))
    if rs_media[h]/(0.7*1366.0*np.cos(np.radians(ang_zen_medio[h]))) > 0:
        t_atm.append(rs_media[h]/(0.7*1366.0*np.cos(np.radians(ang_zen_medio[h]))))   #uso np.radians pois se fizer a regra de 3 simples (ang_zen_medio[h]*np.pi/180) obtenho um erro que diz me que não posso multiplicar uma sequencia por um nº float            
   


x = range(int(round(nascer_do_sol)), int(round(por_do_sol))+1)                                   
y = t_atm
fig , ax= plt.subplots()
plt.plot(x, y, '-o')
ax.set_xlabel(" horas do ciclo diurno ")
ax.set_ylabel(" transmissividade atmosférica ")
plt.show()


