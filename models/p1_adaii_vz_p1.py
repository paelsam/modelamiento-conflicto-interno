import math
import os
from helpers.procesar_pruebas import procesar_pruebas as pp
from models.p1_adaii_fb import ModCI_fb
from models.p1_adaii_pd import ModCI_pd


def conflicto_interno(RS: list[list, int]) -> float:
    grupos = RS[0]
    numerador = sum(sa[0] * (sa[1] - sa[2])**2 for sa in RS[0])
    denominador = len(grupos)
    return numerador / denominador if denominador > 0 else 0.0

def esfuerzo(RS: list[list, int], E: list[int]) -> int:
    return sum(math.ceil(abs(sa[1]-sa[2]) * sa[3] * E[index]) for (index, sa) in enumerate(RS[0]))

def conflicto_modificado(RS: list[list, int], E: list[int]) -> float:
    grupos = RS[0]
    numerador = 0.0
    denominador = len(grupos) 
    
    for i, sa in enumerate(grupos):
        n_i, o1, o2, _ = sa
        e_i = E[i] 
        n_rest = n_i - e_i
        numerador += n_rest * (o1 - o2)**2
    
    return numerador / denominador if denominador > 0 else 0.0

def conflicto_individual(sa, e):
    n, o1, o2 = sa[0], sa[1], sa[2]
    return (n - e) * (o1 - o2)**2

def esfuerzo_individual(sa, e):
    o1, o2, r = sa[1], sa[2], sa[3]
    return math.ceil(abs(o1 - o2) * r * e)

def ModCI_voraz(RS):
    grupos, R_max = RS
    n = len(grupos)
    estrategia = [0] * n
    R_actual = 0

    def prioridad(grupo):
        # print(grupo)
        n, o_i1, o_i2, r = grupo
        return abs(o_i1 - o_i2) / r
        

    # Ordenamos por prioridad descendente
    grupos_ordenados = sorted(
        enumerate(grupos),
        key=lambda x: prioridad(x[1]),
        reverse=True
    )

    for idx, (n_i, o1, o2, r) in grupos_ordenados:
        if R_actual >= R_max:
            break

        d_o = abs(o1 - o2)
        if d_o == 0:
            continue

        # Calculamos el máximo de agentes que podemos modificar
        costo_por_agente = math.ceil(d_o * r)
        if costo_por_agente == 0:
            continue

        max_posible = min(
            n_i,
            (R_max - R_actual) // costo_por_agente
        )

        if max_posible > 0:
            estrategia[idx] = max_posible
            R_actual += max_posible * costo_por_agente

    CI_final = conflicto_modificado(RS, estrategia)
    esfuerzo_final = R_actual  

    return estrategia, CI_final, esfuerzo_final

if __name__ == "__main__":
    
    # Casos de prueba
    
    pruebas = os.listdir('./pruebas/')
    pruebas.sort(key=lambda x: int(x.replace('Prueba', '').replace('.txt', '')))
    lista_pruebas = [ f"./pruebas/{prueba}" for prueba in pruebas]
    lista_porcentajes = []

    for index, candidato in enumerate(lista_pruebas):
        
        print(f"Prueba{index + 1}.txt".center(50, '*'))
        
        candidato = pp(candidato)
        
        print("----- Voraz -----")
        E_vz, conf_vz, cost_vz = ModCI_voraz(candidato)
        print("Estrategia:", E_vz)
        print("Conflicto modificado:", conf_vz)
        print("Esfuerzo:", cost_vz)
        
        # Calculos de las diferencias entre los resultados de la fuerza bruta y el algoritmo voraz
        
        print("")
        print("----- Fuerza Bruta -----")
        E_fbcost_fb, conf_fbcost_fb, cost_fb = ModCI_pd(candidato)
        print("Estrategia FB:", E_fbcost_fb)
        print("Conflicto modificado FB:", conf_fbcost_fb)
        print("Esfuerzo FB:", cost_fb)
        
        print("")
        print("----- Comparación -----")
        print("Diferencia en estrategia:", [E_vz[i] - E_fbcost_fb[i] for i in range(len(E_vz))])
        print("Diferencia en conflicto modificado:", conf_vz - conf_fbcost_fb)
        print("Diferencia en esfuerzo:", cost_vz - cost_fb)
        print("Porcentaje de diferenca de conflicto modificado:", (conf_vz - conf_fbcost_fb) / conf_fbcost_fb * 100 if conf_fbcost_fb > 0 else 0, "%")
        
        diferencia_porcentaje = (conf_vz - conf_fbcost_fb) / conf_fbcost_fb * 100 if conf_fbcost_fb > 0 else 0
        lista_porcentajes.append(diferencia_porcentaje)

        print("\n")
    
    promedio_porcentaje = sum(lista_porcentajes) / len(lista_porcentajes) if lista_porcentajes else 0
    print("Porcentaje promedio de diferencia de conflicto modificado:", promedio_porcentaje, "%")
        
