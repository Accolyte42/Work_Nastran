# Программа для чтения данных расчета из Nastran в формате .f06 (.txt)
# На вход требует полный путь до файла
# На выходе выдает:
# 1) график с построенной скоростью от демпфирования
# 2) График с построенной частотой от демпфирования
# На обоих графиках подписывает текущий расчетный случай: точку и мах
#
#
import pandas as pd


Flut_flag = False
count_point = 3  # номер строки, с которой идет описание случая
count_data = 5  # номер строки, с которой идут данные (с шапкой)
counter = 0
with open('rv_30_surf_all_fl_m09_new.f06') as file:
    for line in file:
        line = line.strip()
        if 'FLUTTER' and 'SUMMARY' in line:
            Flut_flag = True
        while Flut_flag:
            if 'NASTRAN' and 'AEROELASTIC' in line:
                Flut_flag = False
                break
            print(line.strip())
            break













