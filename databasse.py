from typing import Dict, Optional
from datetime import datetime
from .model import AeroportoModel, AeroportoCreate




class Database:
    def __init__(self):
        self._aeroporti: Dict[int, AeroportoModel] = {}
        self._counter = 1
        self._init_data()

    def _init_data(self):

        sample_airports = [
            {"codice": "MXP", "citta": "Milano"},
            {"codice": "BGY", "citta": "Bergamo"},
            {"codice": "FCO", "citta": "Roma"},
            {"codice": "LIN", "citta": "Milano Linate"},
            {"codice": "VCE", "citta": "Venezia"},
            {"codice": "BLQ", "citta": "Bologna"},
            {"codice": "NAP", "citta": "Napoli"},
            {"codice": "CTA", "citta": "Catania"},
            {"codice": "PMO", "citta": "Palermo"},
            {"codice": "TRN", "citta": "Torino"},
            {"codice": "GOA", "citta": "Genova"},
            {"codice": "CTA", "citta": "Catania"}
        ]

        for airport in sample_airports:
            self.create(AeroportoCreate(**airport))

    def create(self, aeroporto: AeroportoCreate) -> AeroportoModel:

        for existing in self._aeroporti.values():
            if existing.codice == aeroporto.codice:
                raise ValueError(f"Aeroporto con codice {aeroporto.codice} già esistente")

        new_id = self._counter
        self._counter += 1

        new_aeroporto = AeroportoModel(
            id=new_id,
            codice=aeroporto.codice,
            citta=aeroporto.citta,
            created_at=datetime.now()
        )

        self._aeroporti[new_id] = new_aeroporto
        return new_aeroporto

    def get_all(self, page: int = 1, size: int = 10) -> tuple[list[AeroportoModel], int]:

        start = (page - 1) * size
        end = start + size

        all_items = list(self._aeroporti.values())
        total = len(all_items)
        data = all_items[start:end]

        return data, total

    def get_by_id(self, id: int) -> Optional[AeroportoModel]:

        return self._aeroporti.get(id)

    def delete(self, id: int) -> bool:

        if id in self._aeroporti:
            del self._aeroporti[id]
            return True
        return False

    def update(self, id: int, aeroporto: AeroportoCreate) -> Optional[AeroportoModel]:

        if id not in self._aeroporti:
            return None


        for existing in self._aeroporti.values():
            if existing.id != id and existing.codice == aeroporto.codice:
                raise ValueError(f"Aeroporto con codice {aeroporto.codice} già esistente")

        return aeroporto

db = Database()