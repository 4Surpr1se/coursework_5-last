from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self) -> bool:
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough():
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = 'УДАР ЯРОСТИ'
    stamina = 3
    damage = 7

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.hp = round(self.target.hp - self.damage, 2)
        return f'Навык {self.name} игрока {self.user.name} успешно нанес {self.damage} противнику.'


class HardShot(Skill):
    name = 'Меткий выстрел'
    stamina = 20
    damage = 8

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.hp = round(self.target.hp - self.damage, 2)
        return f'Навык {self.name} игрока {self.user.name} успешно нанес {self.damage} противнику.'


fury_punch = FuryPunch()
hard_shot = HardShot()
