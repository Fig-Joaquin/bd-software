from database_manager.mongodb_manager import MongoDBManager

def main():
    mongodb_manager = MongoDBManager()
    file_path = 'data/file-data.csv'  # Ruta correcta al archivo CSV
    mongodb_manager.load_data_from_csv('data_eng_salaries', file_path)
    print("Datos cargados exitosamente.")

if __name__ == "__main__":
    main()
