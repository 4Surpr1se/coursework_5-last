import dataclasses
from dataclasses import dataclass
from skills import Skill, FuryPunch, HardShot
import marshmallow_dataclass

warrior_data ={"name": "воин",
               "max_health": 60.0,
               "max_stamina": 30.0,
               "attack": 1.2,
               "stamina": 0.8,
               "armor": 2,
               'skill': FuryPunch()
               }


thief_data ={"name": "вор",
               "max_health": 50.0,
               "max_stamina": 25.0,
               "attack": 1.0,
               "stamina": 1.1,
               "armor": 0.5,
               'skill': HardShot
               }

@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill = dataclasses.field(default=Skill)


warrior_schema = marshmallow_dataclass.class_schema(UnitClass)
WarriorClass = warrior_schema().load(warrior_data) # TODO Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов

# TODO действуем так же как и с войном
thief_schema = marshmallow_dataclass.class_schema(UnitClass)
ThiefClass = warrior_schema().load(thief_data)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}



# print(WarriorClass, '\n', ThiefClass)