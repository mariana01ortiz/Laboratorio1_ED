import json
import os

class SettingsRepository:
    # Repositorio de configuraciones del juego usando JSON
    def __init__(self, filename="settings.json"):
        self.store_file = filename
        self.table = {}  # índice rápido por key
        self._load_store()
        self._rebuild_index()

    # Cargar store desde JSON o inicializar vacío
    def _load_store(self):
        if os.path.exists(self.store_file):
            try:
                with open(self.store_file, "r", encoding="utf-8") as f:
                    self.store = json.load(f)
            except json.JSONDecodeError:
                print("WARNING: JSON corrupto, se reinicia store")
                self.store = []
        else:
            self.store = []

    # Guardar store completo en JSON
    def _save_store(self):
        with open(self.store_file, "w", encoding="utf-8") as f:
            json.dump(self.store, f, indent=4)

    # Reconstruir índice interno por clave
    def _rebuild_index(self):
        self.table.clear()
        for record in self.store:
            key = record.get("key")
            if key:
                self.table[key] = record

    # Obtener configuración por clave
    def get_settings(self, key):
        record = self.table.get(key)
        if not record:
            return None
        return {
            "data": {
                "volume": int(record.get("volume", 50)),
                "difficulty": record.get("difficulty", "Easy"),
                "fullscreen": bool(record.get("fullscreen", False))
            }
        }

    # Guardar o actualizar configuración
    def save_settings(self, key, volume, difficulty, fullscreen):
        existing = self.table.get(key)
        if existing:
            existing["volume"] = volume
            existing["difficulty"] = difficulty
            existing["fullscreen"] = fullscreen
        else:
            # Crear nuevo registro
            new_record = {
                "player_id": "player1",
                "name": "Nataly",
                "score": 200,
                "max_score": 1200,
                "type": "settings",
                "key": key,
                "volume": volume,
                "difficulty": difficulty,
                "fullscreen": fullscreen
            }
            self.store.append(new_record)
        self._save_store()
        self._rebuild_index()

# Retorna la configuración principal del juego
def get_settings_data():
    repo = SettingsRepository()
    data = repo.get_settings("game_settings")
    if data is None:
        return {"volume": 50, "difficulty": "Easy", "fullscreen": False}
    return {
        "volume": data["data"]["volume"],
        "difficulty": data["data"]["difficulty"],
        "fullscreen": data["data"]["fullscreen"]
    }