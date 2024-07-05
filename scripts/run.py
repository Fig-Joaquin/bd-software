from database_manager.db_selector import select_database
from database_manager.mongodb_manager import MongoDBManager

def main():
    while True:
        db_choice = select_database()
        
        if db_choice == "mongodb":
            mongodb_manager = MongoDBManager()
            mongo_menu(mongodb_manager)
        elif db_choice == "neo4j":
            print("Funcionalidad para Neo4j no implementada aún.")
            # Aquí se podría implementar el menú para Neo4j en el futuro
        else:
            print("Selección inválida, terminando programa.")
            break

def mongo_menu(mongodb_manager):
    while True:
        print("\nMenú de MongoDB")
        print("1. Insertar documento desde JSON")
        print("2. Consultas de salarios")
        print("3. Salir")
        
        option = input("Seleccione una opción: ")
        
        if option == "1":
            insertar_json(mongodb_manager)
        elif option == "2":
            consultas_salarios(mongodb_manager)
        elif option == "3":
            print("Saliendo del menú de MongoDB...")
            break
        else:
            print("Opción inválida, intente nuevamente.")

def insertar_json(mongodb_manager):
    file_path = 'data/file-data.json'  # Ruta predeterminada al archivo JSON
    collection_name = 'data_eng_salaries'
    try:
        mongodb_manager.load_data_from_json(collection_name, file_path)
        print("Datos cargados exitosamente.")
    except Exception as e:
        print(f"Error al cargar datos: {e}")

def consultas_salarios(mongodb_manager):
    while True:
        print("\nMenú de Consultas de Salarios")
        print("1. Diferencia de salario entre los niveles de desarrolladores")
        print("2. Lugares con mayor salario según nivel de experiencia")
        print("3. ¿USA es el país con mejores salarios?")
        print("4. Salario promedio global")
        print("5. Área informática con mayor sueldo")
        print("6. Volver al menú principal")
        
        option = input("Seleccione una opción: ")
        
        if option == "1":
            diferencia_salario(mongodb_manager)
        elif option == "2":
            lugares_mayor_salario(mongodb_manager)
        elif option == "3":
            usa_mejores_salarios(mongodb_manager)
        elif option == "4":
            salario_promedio_global(mongodb_manager)
        elif option == "5":
            area_mayor_sueldo(mongodb_manager)
        elif option == "6":
            break
        else:
            print("Opción inválida, intente nuevamente.")

def diferencia_salario(mongodb_manager):
    collection_name = 'data_eng_salaries'
    pipeline = [
        {"$match": {"salary_currency": "USD"}},
        {"$group": {"_id": "$experience_level", "avg_salary": {"$avg": "$salary_in_usd"}}},
        {"$sort": {"avg_salary": -1}}
    ]
    result = mongodb_manager.find_documents_with_aggregate(collection_name, pipeline)
    print("Diferencia de salario entre los niveles de desarrolladores (USD):")
    if not result:
        print("No se encontraron datos.")
    for item in result:
        print(f"Nivel: {item['_id']}, Salario Promedio: {format_currency(item['avg_salary'])} USD")

def lugares_mayor_salario(mongodb_manager):
    collection_name = 'data_eng_salaries'
    pipeline = [
        {"$match": {"salary_currency": "USD"}},
        {"$group": {"_id": {"experience_level": "$experience_level", "location": "$employee_residence"}, "avg_salary": {"$avg": "$salary_in_usd"}}},
        {"$sort": {"_id.experience_level": 1, "avg_salary": -1}}
    ]
    result = mongodb_manager.find_documents_with_aggregate(collection_name, pipeline)
    print("\nLugares con mayor salario según nivel de experiencia (USD):")
    if not result:
        print("No se encontraron datos.")
    for item in result:
        location = item['_id'].get('location', 'Desconocido')
        print(f"Nivel: {item['_id']['experience_level']}, Lugar: {location}, Salario Promedio: {format_currency(item['avg_salary'])} USD")

def usa_mejores_salarios(mongodb_manager):
    collection_name = 'data_eng_salaries'
    pipeline_usa = [
        {"$match": {"employee_residence": "US", "salary_currency": "USD"}},
        {"$group": {"_id": None, "avg_salary_usa": {"$avg": "$salary_in_usd"}}}
    ]
    salario_usa = mongodb_manager.find_documents_with_aggregate(collection_name, pipeline_usa)
    avg_salary_usa = salario_usa[0]['avg_salary_usa'] if salario_usa else 0

    pipeline_global = [
        {"$match": {"salary_currency": "USD"}},
        {"$group": {"_id": None, "avg_salary_global": {"$avg": "$salary_in_usd"}}}
    ]
    salario_global = mongodb_manager.find_documents_with_aggregate(collection_name, pipeline_global)
    avg_salary_global = salario_global[0]['avg_salary_global'] if salario_global else 0

    print("\n¿USA es el país con mejores salarios?")
    print(f"Salario Promedio USA: {format_currency(avg_salary_usa)} USD")
    print(f"Salario Promedio Global: {format_currency(avg_salary_global)} USD")

def salario_promedio_global(mongodb_manager):
    collection_name = 'data_eng_salaries'
    pipeline = [
        {"$match": {"salary_currency": "USD"}},
        {"$group": {"_id": None, "avg_salary_global": {"$avg": "$salary_in_usd"}}}
    ]
    result = mongodb_manager.find_documents_with_aggregate(collection_name, pipeline)
    avg_salary_global = result[0]['avg_salary_global'] if result else 0
    print(f"\nSalario Promedio Global (USD): {format_currency(avg_salary_global)} USD")

def area_mayor_sueldo(mongodb_manager):
    collection_name = 'data_eng_salaries'
    pipeline = [
        {"$match": {"salary_currency": "USD"}},
        {"$group": {"_id": "$job_title", "avg_salary": {"$avg": "$salary_in_usd"}}},
        {"$sort": {"avg_salary": -1}},
        {"$limit": 1}
    ]
    result = mongodb_manager.find_documents_with_aggregate(collection_name, pipeline)
    area_con_mayor_sueldo = result[0] if result else {"_id": "N/A", "avg_salary": 0}
    print("\nÁrea informática con mayor sueldo (USD):")
    print(f"Área: {area_con_mayor_sueldo['_id']}, Salario Promedio: {format_currency(area_con_mayor_sueldo['avg_salary'])} USD")

def format_currency(value):
    return f"{value:,.2f}"

if __name__ == "__main__":
    main()
