#Leitura do ficheiro, e transformação de dados em dicionários:
#Tirar comentário de linhas de json
import json
import datetime
import math

EjetLatitude = 32.61
EjetLongitude = -16.71
DeclinacaoSol = {}

token = open("AG1.txt","r")
anos = {}
anos['Year'] = []
meses = {}
meses['Months'] = []
dias = {}
dias['Days'] = []
hours = {}
hours['Hours'] = []
t2 = {}
t2['T2'] = []
swdown = {}
swdown['SWDOWN'] = []
lwdown = {}
lwdown['LWDOWN'] = []
u10 = {}
u10['U10'] = []
v10 = {}
v10['V10'] = []

linestoken = token.readlines()
tokens_column = 0

for x in linestoken:
    anos['Year'].append(x.split()[tokens_column])
del anos['Year'][0]

tokens_column = 1
for y in linestoken:
    if (y.split()[tokens_column] != "mm"):
        if (int(y.split()[tokens_column]) < 10):
            meses['Months'].append(y.split()[tokens_column].zfill(2))
        else:
            meses['Months'].append(y.split()[tokens_column])
del meses['Months'][0]

tokens_column = 2
for y in linestoken:
    if(y.split()[tokens_column] != "dd"):
        if(int(y.split()[tokens_column]) < 10):
            dias['Days'].append(y.split()[tokens_column].zfill(2))
        else:
            dias['Days'].append(y.split()[tokens_column])
del dias['Days'][0]

tokens_column = 3
for y in linestoken:
    hours['Hours'].append(y.split()[tokens_column])
del hours['Hours'][0]

tokens_column = 4
for y in linestoken:
    t2['T2'].append(y.split()[tokens_column])
del t2['T2'][0]

tokens_column = 5
for y in linestoken:
    swdown['SWDOWN'].append(y.split()[tokens_column])
del swdown['SWDOWN'][0]

tokens_column = 6
for y in linestoken:
    lwdown['LWDOWN'].append(y.split()[tokens_column])
del lwdown['LWDOWN'][0]

tokens_column = 7
for y in linestoken:
    u10['U10'].append(y.split()[tokens_column])
del u10['U10'][0]

tokens_column = 8
for y in linestoken:
    v10['V10'].append(y.split()[tokens_column])
del v10['V10'][0]
token.close()

w = []
list1 = hours["Hours"]


for hour in list1:
    AnguloHorario = (int(hour) - 12) * (360/24) + EjetLongitude
    w.append(round(AnguloHorario,3))


fmt = "%Y.%m.%d"
list2 = anos["Year"]
list3 = meses['Months']
list4 = dias['Days']
ListOfNewDates = []
NewCount = 0;
for i in list4:
    ListOfNewDates.append(list2[NewCount] + "." + list3[NewCount] + "." + list4[NewCount])
    NewCount = NewCount + 1

ListOfJulianDays = []
CountDates = 0;
for i in ListOfNewDates:
    dt = datetime.datetime.strptime(ListOfNewDates[CountDates], fmt)
    tt = dt.timetuple()
    ListOfJulianDays.append(tt.tm_yday)
    CountDates = CountDates + 1

Sin_DeclinacaoSol = []
CountDec1 = 0
for i in ListOfJulianDays:
    CalculoSinDecSol = -0.39779 * math.cos(0.98565 * (ListOfJulianDays[CountDec1]+10)+1.914*math.sin(0.98565 * (ListOfJulianDays[CountDec1]-2)))
    Sin_DeclinacaoSol.append(CalculoSinDecSol)
    CountDec1 = CountDec1 + 1

AngulosDeclinaçãoSol = []
CountAngulos = 0
for i in Sin_DeclinacaoSol:
    AngulosDeclinaçãoSol.append(math.asin(Sin_DeclinacaoSol[CountAngulos]))
    CountAngulos = CountAngulos + 1

CosAnguloZenital = []
CountCosAngZen = 0
for i in AngulosDeclinaçãoSol:
    AnguloDeclinacaoSol = AngulosDeclinaçãoSol[CountCosAngZen]
    NewAnguloHorario = w[CountCosAngZen]
    CalculoCosAngZen = math.sin(EjetLatitude) * math.sin(AnguloDeclinacaoSol) + math.cos(EjetLatitude) * math.cos(AnguloDeclinacaoSol) * math.cos(NewAnguloHorario)
    CosAnguloZenital.append(CalculoCosAngZen)
    CountCosAngZen = CountCosAngZen + 1

AnguloZenital = []
CountAngZen = 0
for i in CosAnguloZenital:
    CalcAngZen = math.acos(AngulosDeclinaçãoSol[CountAngZen])
    AnguloZenital.append(CalcAngZen)
    CountAngZen = CountAngZen + 1



# Caso seja necessário escrever nos ficheiros texto
#
with open('AnguloZenital','w') as jsonfile:
    json.dump(AnguloZenital,jsonfile)

#with open('SinDecliSol','w') as jsonfile:
#    json.dump(Sin_DeclinacaoSol,jsonfile)
#with open('AngulosHorarios','w') as jsonfile:
#    json.dump(w,jsonfile)
#with open('years.txt','w') as jsonfile:
#    json.dump(anos,jsonfile);
#with open('months.txt', 'w') as jsonfile:
#    json.dump(meses, jsonfile);
#with open('days.txt', 'w') as jsonfile:
#    json.dump(dias, jsonfile);
#with open('hours.txt', 'w') as jsonfile:
#    json.dump(hours, jsonfile);
#with open('t2.txt', 'w') as jsonfile:
#    json.dump(t2, jsonfile);
#with open('swdown.txt', 'w') as jsonfile:
#    json.dump(swdown, jsonfile);
#with open('lwdown.txt', 'w') as jsonfile:
#    json.dump(lwdown, jsonfile);
#with open('u10.txt', 'w') as jsonfile:
#    json.dump(u10, jsonfile);
#with open('v10.txt', 'w') as jsonfile:
#    json.dump(v10, jsonfile);





