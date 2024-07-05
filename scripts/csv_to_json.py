import csv
import json

csv_file_path = 'data/file-data.csv'
json_file_path = 'data/file-data.json'

def csv_to_json(csv_file_path, json_file_path):
    data = []
    
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            data.append(row)
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

csv_to_json(csv_file_path, json_file_path)
print("CSV convertido a JSON exitosamente.")
