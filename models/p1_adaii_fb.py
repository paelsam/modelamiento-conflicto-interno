import math
from helpers.procesar_pruebas import procesar_pruebas as pp

# Función para calcular el conflicto interno (No se usa)
def conflicto_interno(RS: list[list, int]) -> int:
    return sum([sa[0]*(sa[1] - sa[2])**2 for sa in RS[0]]) / sum([sa[0] for sa in RS[0]])

# Función para calcular el esfuerzo
def esfuerzo(RS: list[list, int], E: list[int]) -> int:
    return sum([math.ceil(abs(sa[1]-sa[2]) * sa[3] * E[index]) for (index, sa) in  enumerate(RS[0])])

# Función que calcula el conflicto luego de aplicar la estrategia E
def conflicto_modificado(RS, E):
    grupos = RS[0]
    num = 0
    den = len(grupos)
    for i, sa in enumerate(grupos):
        n_i, o1, o2, _ = sa
        # Quedan (n_i - e_i) agentes en el grupo
        n_rest = n_i - E[i]
        num += n_rest * (o1 - o2)**2
    return num/den if den > 0 else 0.0


def ModCI_fb(RS):
    grupos = RS[0]
    R_max = RS[1]
    n = len(grupos)
    mejor_estrategia = None
    mejor_ci = float('inf')
    mejor_esfuerzo = None

    # Función recursiva para enumerar combinaciones de e_i en cada grupo.
    def backtrack(i: int, current_E: list[int]):
        nonlocal mejor_estrategia, mejor_ci, mejor_esfuerzo
        if i == n:
            esfuerzo_total = esfuerzo(RS, current_E)
            if esfuerzo_total <= R_max:
                conf = conflicto_modificado(RS, current_E)
                # Actualizar si se mejora
                if conf < mejor_ci:
                    mejor_ci = conf
                    mejor_estrategia = current_E.copy()
                    mejor_esfuerzo = esfuerzo_total
            return
        
        n_i: int = grupos[i][0]
        for e in range(n_i + 1):
            current_E.append(e)
            backtrack(i+1, current_E)
            current_E.pop()
    
    backtrack(0, [])
    return mejor_estrategia, mejor_ci, mejor_esfuerzo

if __name__ == "__main__":
    
    # Casos de prueba
    
    prueba1 = pp("./pruebas/Prueba1.txt")
    prueba2 = pp("./pruebas/Prueba2.txt")
    prueba3 = pp("./pruebas/Prueba3.txt")
    prueba4 = pp("./pruebas/Prueba4.txt")
    prueba5 = pp("./pruebas/Prueba5.txt")
    prueba6 = pp("./pruebas/Prueba6.txt")
    prueba7 = pp("./pruebas/Prueba7.txt")
    prueba8 = pp("./pruebas/Prueba8.txt")
    prueba10 = pp("./pruebas/Prueba10.txt")
    prueba11 = pp("./pruebas/Prueba11.txt")

    print("----- Fuerza Bruta -----")
    E_fb, conf_fb, cost_fb = ModCI_fb(prueba7)
    print("Estrategia:", E_fb)
    print("Conflicto modificado:", conf_fb)
    print("Esfuerzo:", cost_fb)




