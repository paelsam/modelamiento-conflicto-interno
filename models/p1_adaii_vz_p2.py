import math
import os
from helpers.procesar_pruebas import procesar_pruebas as pp
from models.p1_adaii_pd import ModCI_pd
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

def ModCI_voraz(RS):
    grupos, R_max = RS
    n = len(grupos)
    estrategia = [0] * n
    R_actual = 0

    def prioridad(grupo):
        _, o1, o2, r = grupo
        d_o = abs(o1 - o2)
        if d_o == 0:
            return 0.0
        costo_por_agente = math.ceil(d_o * r)
        if costo_por_agente == 0:
            return float('inf')
        print((d_o ** 2) / costo_por_agente)
        return (d_o ** 2) / costo_por_agente  # Prioridad por agente

    # Ordenar grupos con la prioridad como criterio
    grupos_ordenados = sorted(
        enumerate(grupos),
        key=lambda x: prioridad(x[1]),
        reverse=True
    )

    for idx_original, grupo in grupos_ordenados:
        if R_actual >= R_max:
            break
        n_i, o1, o2, r = grupo
        d_o = abs(o1 - o2)
        if d_o == 0:
            continue
        
        costo_por_agente = math.ceil(d_o * r)
        if costo_por_agente == 0:
            max_posible = n_i
        else:
            max_posible = min(
                n_i,
                (R_max - R_actual) // costo_por_agente
            )
        
        if max_posible > 0:
            estrategia[idx_original] = max_posible
            R_actual += max_posible * costo_por_agente

    return estrategia, conflicto_modificado(RS, estrategia), R_actual

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
        print("----- Programación dinámica -----")
        E_pdcost_pd, conf_pdcost_pd, cost_pd = ModCI_pd(candidato)
        print("Estrategia PD:", E_pdcost_pd)
        print("Conflicto modificado PD:", conf_pdcost_pd)
        print("Esfuerzo PD:", cost_pd)
        
        print("")
        print("----- Comparación -----")
        print("Diferencia en estrategia:", [E_vz[i] - E_pdcost_pd[i] for i in range(len(E_vz))])
        print("Diferencia en conflicto modificado:", conf_vz - conf_pdcost_pd)
        print("Diferencia en esfuerzo:", cost_vz - cost_pd)
        print("Porcentaje de diferenca de conflicto modificado:", (conf_vz - conf_pdcost_pd) / conf_pdcost_pd * 100 if conf_pdcost_pd > 0 else 0, "%")
        
        diferencia_porcentaje = (conf_vz - conf_pdcost_pd) / conf_pdcost_pd * 100 if conf_pdcost_pd > 0 else 0
        lista_porcentajes.append(diferencia_porcentaje)

        print("\n")
    
    promedio_porcentaje = sum(lista_porcentajes) / len(lista_porcentajes) if lista_porcentajes else 0
    print("Porcentaje promedio de diferencia de conflicto modificado:", promedio_porcentaje, "%")