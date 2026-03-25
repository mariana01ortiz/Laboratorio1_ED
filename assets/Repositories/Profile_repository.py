from Persistence.Hash_table import HashTable
import time
import random
import string
import os
import json

class RecordStoreJSON:
    # Store de perfiles usando JSON
    def __init__(self, filename="profiles.json"):
        self.filename = filename
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
            except json.JSONDecodeError:
                self.records = []
        else:
            self.records = []

    # Retorna todos los registros
    def get_all_records(self):
        return self.records

    # Agrega un nuevo registro y retorna el índice
    def add_record(self, record):
        self.records.append(record)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=4)
        return len(self.records) - 1  # índice en la lista

class ProfileRepository:
    # Repositorio de perfiles usando JSON y HashTable
    def __init__(self):
        self.table = HashTable(capacity=5000)
        self.store = RecordStoreJSON()

        for i, record in enumerate(self.store.records):
            self.table.insert(record["id"], i)
            
    # Guardar perfil
    def save_profile(self, player_id, name, score, max_score):
        record = {
            "id": player_id,
            "name": name,
            "score": score,
            "max_score": max_score
        }
        position = self.store.add_record(record)
        self.table.insert(player_id, position)

    # Obtener perfil por id
    def get_profile(self, player_id):
        position = self.table.search(player_id)
        if position == -1:
            return None
        try:
            return self.store.records[position]
        except IndexError:
            return None

    # Generar siguiente id
    def get_next_id(self):
        records = self.store.get_all_records()
        if not records:
            return "player1"
        last_id = records[-1]["id"]
        number = int(last_id.replace("player", ""))
        return f"player{number + 1}"

    # Retornar todos los perfiles
    def get_all_profiles(self):
        return self.store.get_all_records()

# Generar nombres aleatorios
def random_name(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Benchmark de inserción y búsqueda
def run_benchmark(num_records=5000, num_search=1000):
    repo = ProfileRepository()
    repo.store.records = []  # limpiar store

    # Inserción
    start_insert = time.perf_counter()
    for _ in range(num_records):
        player_id = repo.get_next_id()
        name = random_name()
        score = random.randint(0, 1000)
        max_score = score + random.randint(0, 1000)
        repo.save_profile(player_id, name, score, max_score)
    end_insert = time.perf_counter()
    insertion_time = end_insert - start_insert

    # Búsqueda
    search_ids = [f"player{random.randint(1, num_records)}" for _ in range(num_search)]
    start_search = time.perf_counter()
    for pid in search_ids:
        _ = repo.get_profile(pid)
    end_search = time.perf_counter()
    search_time_avg = (end_search - start_search) / len(search_ids)

    # Métricas HashTable
    collisions = getattr(repo.table, "collisions", "No implementado")
    load_factor = (getattr(repo.table, "count", 0) / repo.table.capacity) if hasattr(repo.table, "count") else "No implementado"

    # Resultados
    print(f"Tiempo total de inserción ({num_records} registros): {insertion_time:.4f} s")
    print(f"Tiempo promedio de búsqueda ({num_search} consultas): {search_time_avg:.6f} s")
    print(f"Número de colisiones: {collisions}")
    print(f"Factor de carga: {load_factor:.4f}")

if __name__ == "__main__":
    run_benchmark()  