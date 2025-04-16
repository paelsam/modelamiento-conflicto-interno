import math
from helpers.procesar_pruebas import procesar_pruebas as pp

def esfuerzo_individual(sa, e):
    o1, o2, r = sa[1], sa[2], sa[3]
    return math.ceil(abs(o1 - o2) * r * e)

def conflicto_individual(sa, e):
    n, o1, o2 = sa[0], sa[1], sa[2]
    return (n - e) * (o1 - o2)**2

def ModCI_pd(RS):
    grupos = RS[0]
    R_max = RS[1]
    n = len(grupos)

    MCI = [[float('inf')] * (R_max + 1) for _ in range(n + 1)]
    MCI[0][0] = 0  

    decision = [[-1] * (R_max + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for r in range(R_max + 1):
            for e in range(grupos[i-1][0] + 1):
                esf = esfuerzo_individual(grupos[i-1], e)
                conf = conflicto_individual(grupos[i-1], e)
                if r >= esf and MCI[i-1][r - esf] + conf < MCI[i][r]:
                    MCI[i][r] = MCI[i-1][r - esf] + conf
                    decision[i][r] = e
        
    mejor_ci = float('inf')
    mejor_esfuerzo = -1
    for r in range(R_max + 1):
        if MCI[n][r] < mejor_ci:
            mejor_ci = MCI[n][r]
            mejor_esfuerzo = r

    E = []
    r = mejor_esfuerzo
    for i in range(n, 0, -1):
        e = decision[i][r]
        E.append(e)
        r -= esfuerzo_individual(grupos[i-1], e)
    E.reverse()
    
    # print("----- Matriz de Conflicto Modificado -----")
    # for i in range(n + 1):
    #     for j in range(R_max + 1):
    #         print(f"{MCI[i][j]:<5}", end=" ")
    #     print()
    # print("----- Decisiones -----")
    # for i in range(n + 1):
    #     for j in range(R_max + 1):
    #         print(f"{decision[i][j]:<5}", end=" ")
    #     print()
    # print("----- Conflicto -----")
    # print(mejor_ci)
    # print("----- Esfuerzo -----")
    # print(mejor_esfuerzo)

    return E, mejor_ci / n, mejor_esfuerzo


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

    print("----- Programación dinámica -----")
    # E_fb, conf_fb, cost_fb = ModCI_pd(prueba7)
    E_fb, conf_fb, cost_fb = ModCI_pd([[[1,-10,10,0.2], [2,5,-1,0.3]], 5])
    # E_fb, conf_fb, cost_fb = ModCI_pd([[[3,-100,50,0.5], [1,100,80,0.1], [1,-10,0,0.5]], 80])
    print("Estrategia:", E_fb)
    print("Conflicto modificado:", conf_fb)
    print("Esfuerzo:", cost_fb)
