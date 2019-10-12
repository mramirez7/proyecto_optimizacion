from random import randint
from gurobipy import *

# Conjuntos
pacientes = [i for i in range(100)]
modulos = [i for i in range(24)]
doctores = [i for i in range(30)]
tratamientos = [i for i in range(15)]

# Parametros
alpha_d = [randint(5, 8) for i in range(30)]
q = 3
b_pmt =[[[0 for i in range(15)] for j in range(24)] for k in range(100)]

for p in pacientes:
    t = randint(0, 14)
    m = randint(0, 23)
    b_pmt[p][m][t] = 1

d_t = list(randint(3,5) for t in tratamientos)

combinaciones_pdm = []
for paciente in pacientes:
    for doctor in doctores:
        for modulo in modulos:
            combinaciones_pdm.append((paciente, doctor, modulo))
combinaciones_pdm = tuplelist(combinaciones_pdm)

combinaciones_dm = []
for doctor in doctores:
    for modulo in modulos:
        combinaciones_dm.append((doctor, modulo))

combinaciones_dm = tuplelist(combinaciones_dm)

combinaciones_pd = []
for paciente in pacientes:
    for doctor in doctores:
        combinaciones_pd.append((paciente, doctor))

combinaciones_pd = tuplelist(combinaciones_pd)