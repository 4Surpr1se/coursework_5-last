from classes import unit_classes
from equipment import equipment

result = equipment
result['classes'] = [k for k,v in unit_classes.items()]
result['header'] = 'Выберите Героя'
print(result)
