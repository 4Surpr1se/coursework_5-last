from dataclasses import dataclass
from typing import List, Union, Any
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

@dataclass
class EquipmentData:
    weapons: List[Any]
    armors: List[Any]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()
        self.name = 'adas'

    def get_weapon(self, weapon_name) -> Weapon:
        for x in self.equipment.weapons:
            if x['name'] == weapon_name:
                weapon_schema = marshmallow_dataclass.class_schema(Weapon)
                return weapon_schema().load(x)

    def get_armor(self, armor_name) -> Armor:
        # TODO возвращает объект брони по имени
        for x in self.equipment.armors:
            if x['name'] == armor_name:
                armor_schema = marshmallow_dataclass.class_schema(Armor)
                return armor_schema().load(x)

    def get_weapons_names(self) -> list:
        # TODO возвращаем список с оружием
        return [item['name'] for item in self.equipment.weapons]

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        return [item['name'] for item in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        equipment_file = open("./data/equipment.json", encoding='utf-8')
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError


equipment = {
    'weapons': Equipment().get_weapons_names(),
    'armors': Equipment().get_armors_names()
}
# print(equipment)
