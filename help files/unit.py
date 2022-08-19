from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass, WarriorClass, ThiefClass
from random import randint, uniform
from typing import Optional, Tuple, List


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass, weapon: Weapon, armor: Armor):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used = False

    @property
    def health_points(self) -> str:
        return f'Здоровье {self.name} равно {self.hp}'  # TODO переделать - возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self) -> str:
        return f'Выносливость {self.name} равна {self.stamina}'  # TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon) -> str:
        # TODO присваиваем нашему герою новое оружие
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        # TODO одеваем новую броню
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> List[float, int]:
        damage = [0, 0]
        if self.stamina < self.weapon.stamina_per_hit:
            damage = [0, 3]
            return damage
        attack_damage = (uniform(self.weapon.min_damage, self.weapon.max_damage)) * self.unit_class.attack
        if target.stamina < target.armor.stamina_per_turn:
            self.stamina -= self.weapon.stamina_per_hit
            target.get_damage(attack_damage)
            damage = [attack_damage, 4]
            return damage
        damage = round(attack_damage - target.armor.defence * target.unit_class.armor, 2)
        if damage <= 0:
            damage = [0, 2]
        else:
            damage = [damage, 1]
        self.stamina -= self.weapon.stamina_per_hit
        target.stamina -= target.armor.stamina_per_turn
        target.get_damage(damage[0])
        return damage

    def restore_stamina(self, target: BaseUnit):
        if self.stamina + self.unit_class.stamina < self.unit_class.max_stamina:
            self.stamina += self.unit_class.stamina
        if target.stamina + target.unit_class.stamina < target.unit_class.max_stamina:
            target.stamina += target.unit_class.stamina

    def get_damage(self, damage: float):
        self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if not self._is_skill_used:
            # Я решил, что даже если ты попытался заюзать скилл,
            # но не хватило выносливости, то скилл использовать все равно больше нельзя
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)
        else:
            return f'Навык {self.unit_class.skill.name} уже использовался, больше нельзя'


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        damage = self._count_damage(target)
        if damage[1] == 1:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {round(damage[0], 2)} урона."
        if damage[1] == 2:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        if damage[1] == 3:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        if damage[1] == 4:
            return f"{self.name} используя {self.weapon.name} атакует соперника и наносит {round(damage[0], 2)} урона, {target.name} даже не защищается - у него нет выносливости."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if randint(1, 10) == 1 and not self._is_skill_used:
            return self.use_skill(target)
        damage = self._count_damage(target)
        if damage[1] == 1:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {round(damage[0], 2)} урона."
        if damage[1] == 2:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        if damage[1] == 3:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        if damage[1] == 4:
            return f"{self.name} используя {self.weapon.name} атакует соперника и наносит {round(damage[0], 2)} урона, {target.name} даже не защищается - у него нет выносливости."
