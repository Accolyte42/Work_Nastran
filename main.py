# Программа для чтения данных расчета из Nastran в формате .f06 (.txt)
# На вход требует полный путь до файла
# На выходе выдает:
# 1) график с построенной скоростью от демпфирования
# 2) График с построенной частотой от демпфирования
# На обоих графиках подписывает текущий расчетный случай: точку и мах
#
#
import pandas as pd
import matplotlib.pyplot as plt


Flut_flag = False
count_point = 3  # номер строки, с которой идет описание случая
count_data = 5  # номер строки, с которой идут данные (с шапкой)
counter_row = 0  # счетчик строк для определения информативных
counter_points = 1  # счетчик расчетных точек
points_temp = []  # Расчетные точки. Каждая расчетная точка - двумерный массив

with open('rv_30_surf_all_fl_m09_new.f06') as file:
    for line in file:
        line = line.strip()  # убирание лишних пробелов с начала и конца

        if 'FLUTTER' and 'SUMMARY' in line:  # если встретили нужный блок
            Flut_flag = True
            counter_row = 1  # теперь мы можем считать строки в информативном блоке
            pnt = []  # текущая точка

        while Flut_flag and (counter_row == count_point or counter_row > count_data):  # Пока мы в нужном блоке
            if 'NASTRAN' and 'AEROELASTIC' in line:  # Определение условия выхода из блока
                Flut_flag = False
                points_temp.append(pnt)
                counter_row = 0
                break

            for i in range(10):  # Удаление лишних пробелов. Теперь отделение по одному пробелу
                line = line.replace('  ', ' ')
            line += ' '  # чтобы чтение последнего слова работало

            lst_str = []  # Список, в котором содержатся отдельные слова и числа из строки
            temp_str = ''  # список в котором хранится текущее слово
            for i in range(len(line)):
                if line[i] != ' ':  # Если не конец слова, то собираем всё в текущую подстроку
                    temp_str += line[i]
                elif counter_row > count_data + 1:  # преобразование для чисел если конец слова
                    lst_str.append(float(temp_str))
                    temp_str = ''
                else:  # Если конец слова, но в строке идут не числа (посчитал по f06), то просто записываем
                    lst_str.append(temp_str)
                    temp_str = ''

            l = lst_str  # завел переменную, чтоб следующее дело влезло в одну строку
            if counter_row == count_point:  # для первой строки в блоке запись нужной информации
                lst_str = [l[0] + l[1] + l[2] + ', ' + l[3] + '_' + l[4] + l[5] + l[6]]

            # print(lst_str)  # чисто для красивого вывода
            pnt.append(lst_str)  # прочитали всю строку, значит теперь можно список lst_str записать в текущую точку pnt

            break
        counter_row += 1

print()
# print(points_temp)
print()
points = []
for i in range(len(points_temp)):
    points.append(pd.DataFrame(points_temp[i][2:], columns=points_temp[i][1], dtype=float))
print(points[3])

# points[3].plot('DAMPING', 'FREQUENCY')

fig = plt.figure()
for i in range(len(points_temp)):
    plt.plot(points[i]['DAMPING'], points[i]['FREQUENCY'])
plt.grid()
plt.show()

fig = plt.figure()
for i in range(len(points_temp)):
    plt.plot(points[i]['VELOCITY'], points[i]['DAMPING'])
plt.grid()
plt.show()


# Надо добавить оформление получше, выбор файла и выбор точек. Всё остальное запрятать