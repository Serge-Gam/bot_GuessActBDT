#готово
#в этом файле проводим тесты
from SQLighter import SQLighter
import config

#подключим базу
bd_worker = SQLighter(config.database_name)

#тестим модули
# print(bd_worker.select_all())
#

row=bd_worker.select_single(1)
print(row[4])

print(bd_worker.count_raws())


