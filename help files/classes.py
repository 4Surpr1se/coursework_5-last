from dataclasses import dataclass
from skills import Skill, FuryPunch, HardShot, hard_shot, fury_punch
import marshmallow_dataclass

warrior_data = {"name": "воин",
                "max_health": 60.0,
                "max_stamina": 30.0,
                "attack": 1.2,
                "stamina": 0.8,
                "armor": 2
                }

thief_data = {"name": "вор",
              "max_health": 50.0,
              "max_stamina": 25.0,
              "attack": 1.0,
              "stamina": 1.1,
              "armor": 0.5
              }


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float

    def set_skill(self, skill: Skill) -> Skill:
        self.skill = skill
        return self.skill


warrior_schema = marshmallow_dataclass.class_schema(UnitClass)
WarriorClass = warrior_schema().load(warrior_data)
WarriorClass.set_skill(fury_punch)

thief_schema = marshmallow_dataclass.class_schema(UnitClass)
ThiefClass = warrior_schema().load(thief_data)
ThiefClass.set_skill(hard_shot)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
