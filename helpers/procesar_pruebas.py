def procesar_pruebas(ruta_prueba: str) -> list[list[list[int]], int]:
    with open(ruta_prueba, "r") as file: 
        # Limpiar todos las lineas en blanco y saltos de linea
        lineas = list(map(lambda x: x.strip(), file.readlines()))
        lineas.pop(0)
        SA = []
        for line in lineas[:-1]:
            SA.append([int(x) for x in line.split(",")[:-1]] + [float(line.split(",")[-1])])
        r_max = int(lineas[-1])        
        
        
        
    return [SA, r_max]
        
        
    
    