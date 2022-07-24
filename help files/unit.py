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
    def health_points(self):
        return f'Здоровье {self.name} равно {self.hp}'  # TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return f'Выносливость {self.name} равна {self.stamina}'  # TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> List[float, int]:
        damage = [0, 0]
        if self.stamina < self.weapon.stamina_per_hit:
            damage = [0, 3]
            return damage
        attack_damage = round(uniform(self.weapon.min_damage, self.weapon.max_damage), 2) * self.unit_class.attack
        if target.stamina < target.armor.stamina_per_turn:
            self.stamina -= self.weapon.stamina_per_hit
            target.get_damage(attack_damage)
            damage = [attack_damage, 4]
            return damage
        damage = round(attack_damage - target.armor.defence * target.unit_class.armor, 2)
        if damage < 0:
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


        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        # return damage
        #     `УРОН = УРОН_АТАКУЮЩЕГО - БРОНЯ_ЦЕЛИ
        #
        #     `урон_от_оружия = случайное число в диапазоне(min_damage - max_damage)
        #     `УРОН_АТАКУЮЩЕГО = урон_от_оружия * модификатор_атаки_класса
        #
        #     `БРОНЯ_ЦЕЛИ = надетая_броня * модификатор_брони_класса
        #     `
        pass

    def get_damage(self, damage: float) -> Optional[float]:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        self.hp -= damage
        pass

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
            self.unit_class.skill.use(user=self, target=target)
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
        self.restore_stamina(target)
        # TODO результат функции должен возвращать следующие строки:
        if damage[1] == 1:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        if damage[1] == 2:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        if damage[1] == 3:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        if damage[1] == 4:
            return f"{self.name} используя {self.weapon.name} атакует соперника и наносит {damage[0]} урона, {target.name} даже не защищается - у него нет выносливости."
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
        # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:
        if randint(1,10) == 1 and not self._is_skill_used:
            return self.use_skill(target)
        damage = self._count_damage(target)
        self.restore_stamina(target)
        if damage[1] == 1:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        if damage[1] == 2:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        if damage[1] == 3:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        if damage[1] == 4:
            return f"{self.name} используя {self.weapon.name} атакует соперника и наносит {damage[0]} урона, {target.name} даже не защищается - у него нет выносливости."


user = PlayerUnit('olenin', WarriorClass, Equipment().get_weapon('ножик'), Equipment().get_armor('футболка'))
target = EnemyUnit('bot', ThiefClass, Equipment().get_weapon('топорик'), Equipment().get_armor('кожаная броня'))

print(user.hit(target))
print(user.stamina)
print(user.weapon.stamina_per_hit)