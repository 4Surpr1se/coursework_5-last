from unit import PlayerUnit, EnemyUnit
from equipment import Equipment, equipment
from classes import unit_classes


class Instrument:

    @staticmethod
    def request_info(request):
        weapon = request.form['weapon']
        unit_class = request.form['unit_class']
        name = request.form['name']
        armor = request.form['armor']
        for k, v in unit_classes.items():
            if k == unit_class:
                unit_class = v
        return [name,
                unit_class,
                Equipment().get_weapon(weapon),
                Equipment().get_armor(armor)]

    @staticmethod
    def request_info_player(request):
        info = Instrument().request_info(request)
        return PlayerUnit(*info)

    @staticmethod
    def request_info_enemy(request):
        info = Instrument().request_info(request)
        return EnemyUnit(*info)

    @staticmethod
    def result():
        result = equipment
        result['classes'] = [k for k, v in unit_classes.items()]
        return result

    @staticmethod
    def result_hero():
        res = Instrument().result()
        res['header'] = 'Выберите Героя'
        return res

    @staticmethod
    def result_enemy():
        res = Instrument().result()
        res['header'] = 'Выберите Злодея-Негодяя'
        return res


# a = {'name': 'Kt',
#      'weapon': 'ножик',
#      'armor': 'футболка',
#      'unit_class': 'вор'}
#
# print(Instrument.result_enemy())
