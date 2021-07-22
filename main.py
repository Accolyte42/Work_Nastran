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
counter_row = 0  # счетчик строк для определения информативных
counter_points = 1  # счетчик расчетных точек
points = []  # Расчетные точки. Каждая расчетная точка - двумерный массив

with open('rv_30_surf_all_fl_m09_new.f06') as file:
    for line in file:
        line = line.strip()  # убирание лишних пробелов

        if 'FLUTTER' and 'SUMMARY' in line:  # если встретили нужный блок
            Flut_flag = True
            counter_row = 1
            pnt = []  # текущая точка

        while Flut_flag and (counter_row == count_point or counter_row > count_data):  # Пока мы в нужном блоке
            if 'NASTRAN' and 'AEROELASTIC' in line:  # Определение условия выхода из блока
                Flut_flag = False
                points.append(pnt)
                # print(pnt)
                counter_row = 0
                break

#            num_str = ''

        #    for s in range(len(line)):  # Вычленение чисел из строки
        #        s = ' ' if s == '  ' else True
            for i in range(10):  # Удаление лишних пробелов. Теперь отделение по одному пробелу
                line = line.replace('  ', ' ')
            line += ' '  # чтобы чтение последнего слова работало

            lst_str = []  # Список, в котором содержатся отдельные слова и числа из строки
            temp_str = ''  # список в котором хранится текущее слово
            for i in range(len(line)):
                if line[i] != ' ':
                    temp_str += line[i]
                elif counter_row > count_data + 1:  # преобразование для чисел
                    lst_str.append(float(temp_str))
                    temp_str = ''
                else:
                    lst_str.append(temp_str)
                    temp_str = ''
            l = lst_str
            if counter_row == count_point:  # для первой строки в блоке
                lst_str = [l[0] + l[1] + l[2] + ', ' + l[3] + '_' + l[4] + l[5] + l[6]]
            print(lst_str)
            pnt.append(lst_str)


            # for i in range(len(line)):  # По сути вывод всех элементов из строки
            #     print(line[i], end='')
            # print()
            break
        counter_row += 1

print()
print(points)








