#from gurobipy import *
#importamos parametros
from data import *
P = pacientes
D = doctores
M = modulos
T = tratamientos


# Modelo
m = Model('opti')
# Variables
x_pdm = m.addVars(combinaciones_pdm, vtype=GRB.BINARY)
l_dm = m.addVars(combinaciones_dm, vtype=GRB.BINARY)
y_pd = m.addVars(combinaciones_pd, vtype=GRB.BINARY)
z_dm = m.addVars(combinaciones_dm, vtype=GRB.BINARY)
r_dm = m.addVars(combinaciones_dm, vtype=GRB.BINARY)


# Funcion Objetivo
obj1 = quicksum(
    x_pdm[p, d, m]*m
    for p in pacientes
    for d in doctores
    for m in modulos
)

obj2 = quicksum(
    b_pmt[p][m][t]*(m+d_t[t])
    for p in pacientes
    for m in modulos
    for t in tratamientos
)

m.setObjective(obj1-obj2, GRB.MINIMIZE)

# Restricciones

#1. Cada paciente s ́olo puede tener un doctor asignado.
m.addConstrs((quicksum(y_pd[p,d] for d in D) <= 1 ##TODO arreglar corchetes
for p in P), "R1")

#2. Cada paciente puede ser dado de alta exclusivamente por su doctor acargo

m.addConstrs((x_pdm[p,d,m]<=y_pd[p,d] for m in M for p in P for d in D), "R2")


#3. El doctor debe estar trabajando en el hospital en el m ́odulo correspondiente para dar de altaal paciente

m.addConstrs((x_pdm[p,d,m]<=z_dm[d, m] for m in M for p in P for d in D),"R3")

#4. Un doctor puede dar de alta una vez que el paciente termina su tratamiento.

m.addConstrs((quicksum(m*x_pdm[p, d, m] for m in M) <= b_pmt[p][m_prim][t]*(m_prim + d_t[t]) for m_prim in M
for t in T 
for p in P 
for d in D), "R4")

#5. Un paciente no puede ser dado de alta en m ́as de un modulo

m.addConstrs((quicksum(x_pdm[p,d,m] for m in M) <= 1 for p in P for d in D), "R5")

#6. Un doctor puede dar como m ́aximoqpacientes de alta en un modulo

m.addConstrs((quicksum(x_pdm[p,d,m] for p in P) <= q for d in D for m in M), "R6")

#7. A cada paciente se le asigna un doctor cuando pide hora

m.addConstrs((quicksum(y_pd[p, d] for d in D) == b_pmt[p][m][t] for p in P for m in M for t in T), "R7")

#8.  Definicion de l_dm

m.addConstrs((l_dm[d, m] == 1- z_dm[d, m] for d in D for m in M), "R8")

#9. El doctor no puede estar ocupado cuando da de alta al paciente.

m.addConstrs((l_dm[d, m] >= x_pdm[p, d, m] for m in M for p in P for d in D), "R9")

#11. Un doctor no puede trabajar antes de llegar
#12. Numero de turnos maximos que trabaja el doctor



#####
m.optimize()

print(m.status)
# un profesor no puede estar en dos lugares al mismo tiempo
"""m.addConstrs((
    quicksum(A[(p, c, r, t), m] for c in cursos for r in ramos) <= 1
    for t in dias for m in modulos for p in profesores),
    "R1")"""