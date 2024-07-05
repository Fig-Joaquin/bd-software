def select_database():
    print("Seleccione la base de datos:")
    print("1. MongoDB")
    print("2. Neo4j")
    
    choice = input("Ingrese el número correspondiente a su elección: ")
    
    if choice == "1":
        return "mongodb"
    elif choice == "2":
        return "neo4j"
    else:
        print("Selección inválida, intente nuevamente.")
        return select_database()
