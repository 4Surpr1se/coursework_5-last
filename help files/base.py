from typing import Optional

from unit import BaseUnit, PlayerUnit, EnemyUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    result = []
    battle_result = 'Легендарная Битва В Процессе'

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit):
        self.result = []
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        result = None
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            result = 'Ничья'
        if self.player.hp <= 0:
            result = f'{self.player.name} проиграл битву'
        if self.enemy.hp <= 0:
            result = f'{self.player.name} выиграл битву'

        return result

    def _stamina_regeneration(self):
        player_round_stamina = self.player.stamina + (self.STAMINA_PER_ROUND*self.player.unit_class.stamina)
        if player_round_stamina <= self.player.unit_class.max_stamina:
            self.player.stamina = player_round_stamina

        enemy_round_stamina = self.enemy.stamina + (self.STAMINA_PER_ROUND*self.enemy.unit_class.stamina)
        if enemy_round_stamina <= self.enemy.unit_class.max_stamina:
            self.enemy.stamina = enemy_round_stamina

    def _round_hp_stamina(self):
        self.player.hp = round(self.player.hp, 2)
        self.enemy.hp = round(self.enemy.hp, 2)
        self.player.stamina = round(self.player.stamina, 2)
        self.enemy.stamina = round(self.enemy.stamina, 2)

    def next_turn(self):
        self.result.append(self.enemy.hit(self.player))
        self._stamina_regeneration()
        self._round_hp_stamina()
        self._result_len()
        if self._check_players_hp():
            self._end_game()

    def _result_len(self):
        if len(self.result) > 10:
            self.result = self.result[-10:]

    def _end_game(self):
        self._instances = {}
        self.game_is_running = False
        self.result.append(self._check_players_hp())
        self.battle_result = 'Конец битвы'

    def player_hit(self):
        self.result.append(self.player.hit(self.enemy))
        self.next_turn()

    def player_use_skill(self):
        self.result.append(self.player.use_skill(self.enemy))
        self.next_turn()
