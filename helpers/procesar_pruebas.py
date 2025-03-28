def procesar_pruebas(ruta_prueba: str) -> list[list[list[int]], int]:
    with open(ruta_prueba, "r") as file: 
        combinaciones_posibles = 1
        lineas = list(map(lambda x: x.strip(), file.readlines()))
        lineas.pop(0)
        SA: list[int | float] = []
        for line in lineas[:-1]:
            a = [int(x) for x in line.split(",")[:-1]]
            SA.append(a + [float(line.split(",")[-1])])
            combinaciones_posibles *= a[0] + 1
        r_max = int(lineas[-1])   

    # print(f"Combinaciones posibles de {ruta_prueba}: {combinaciones_posibles}")
                
    return [SA, r_max]  
        
        
    
    