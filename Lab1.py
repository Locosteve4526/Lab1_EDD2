from Clases import* 
T = generate_sample_abb()
T.Recorrido_por_Niveles()
zip_path = "/workspaces/Lab1_EDD2/Prueba.zip"
insert_dataset(T,zip_path, limit = 1)
T.graphTree()

while True:
    op = input("Menú: \n1. Insertar un nodo. \n2. Buscar un nodo. \n3. Eliminar un nodo. \n4. Buscar nodo según criterios. \n5. Mostrar recorrido por niveles. \n6. Salir \n")

    if op == "1": 
        img = input("Ingrese el nombre del archivo a insertar: ")
        dir = input("Ingrese la dirección del archivo: ")
        type = input("Ingrese el tipo del archivo: ")
        
        # Obtener el tamaño del archivo
        try:
            size = os.path.getsize(dir)
            # Insertar el archivo en el árbol AVL
            T.insert(img, type, size, dir)
            print("Archivo insertado correctamente.")
        except FileNotFoundError:
            print("Archivo no encontrado.")
            
    elif op == "2":
        name = input("Inserte el nombre del archivo a buscar: ")
        # Buscar el archivo en el árbol AVL
        result, _ = T.search(name)
        if result:
            print(f"Archivo {name} encontrado.")
            answ = input("¿Desea saber la información del nodo? 1. Si. 2. No: ")
            if answ == "1":
                op2=input("¿Desea conocer el padre, tio o abuelo de un nodo?")
                if op2==1:
                    v=input("De que nodo desea conocer el padre")
                    T.pad(v)
                elif op2==2:
                    v=input("de que nodo desea conocer el tio") 
                    T.tio(v)
                elif op2==3:
                    v=input("de que nodo desea conocer el abuelo")   
                    T.abu(v)
                T.pad(result.data)
                print("El factor de equilibrio es:", result.FE)
                print("El nivel del nodo es", result.altura-1)
        else:
            print(f"Archivo {name} no encontrado.")



    elif op == "3":
        name = input("Inserte el nombre del archivo a eliminar: ")
        # Eliminar el archivo del árbol AVL
        deleted = T.delete(name)
        if deleted:
            print(f"Archivo {name} eliminado.")
        else:
            print(f"Archivo {name} no encontrado.")
    elif op == "4":
        
        type = input("Ingrese el tipo de archivos ")
        min_size = int(input("Ingrese el valor mínimo del peso del archivo "))
        max_size = int(input("Ingrese el valor máximo del peso del archivo "))
        result_nodes = T.find_nodes_with_criteria(type, min_size, max_size)
        if result_nodes:
            for node in result_nodes:
                print(node.data)
        else:
            print("No se encontraron nodos que cumplan con los criterios especificados.")
    elif op == "5": 
        # Mostrar recorrido por niveles
        print("Recorrido por niveles:")
        T.Recorrido_por_Niveles()
    elif op == "6":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Intente nuevamente.")





