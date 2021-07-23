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
# %matplotlib qt


def get_points(filename, clear_columns=True):
    # Функция, принимающая (полное) имя файла, и выдающая словарь со всеми
    Flut_flag = False  # Флаг, отвечающий за начало расчета на флаттер в f06 файле
    count_point = 3  # номер строки, с которой идет описание случая
    count_data = 5  # номер строки, с которой идут данные (с шапкой)
    counter_row = 0  # счетчик строк для определения информативных
    points_temp = []  # Расчетные точки. Каждая расчетная точка - двумерный массив
    points_name_subcase = []
    pnt_lst='all'

    # После чтения всего файла получаем points_temp - это все расчетные точки подряд для всех махов (subcase-ов)
    with open(filename) as file:
        for line in file:
            line = line.strip()  # убирание лишних пробелов с начала и конца

            if 'FLUTTER' and 'SUMMARY' in line:  # если встретили нужный блок с началом флаттера
                Flut_flag = True  # Если начался флаттерная часть
                counter_row = 1  # теперь мы можем считать строки в информативном блоке
                pnt = []  # текущая точка

            # Пока мы в нужном блоке
            while Flut_flag and (counter_row == count_point or counter_row > count_data):  # Пока мы в нужном блоке
                if 'NASTRAN' and 'AEROELASTIC' in line:  # Определение условия выхода из блока
                    Flut_flag = False
                    points_temp.append(pnt)  #
                    counter_row = 0
                    break

                for i in range(20):  # Удаление лишних пробелов. Теперь отделение по одному пробелу
                    line = line.replace('  ', ' ')
                line += ' '  # чтобы чтение последнего слова работало

                lst_str = []  # Список, в котором содержатся отдельные слова и числа из строки
                temp_str = ''  # строка, в которой хранится текущее слово
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

                pnt.append(lst_str)  # прочитали всю строку, теперь можно список lst_str записать в текущую точку pnt

                break
            counter_row += 1

    # Далее надо разделить points_temp по сабкейсам (разным махам)
    points = []  # 'nj e;t
    cur_mach = points_temp[0][0][0][points_temp[0][0][0].index('MACH_NUMBER'):]
    dict_points = {}

    # Далее неразделенные записи points_temp деляться на записи по сабкейсам в словарь
    for i in range(len(points_temp)):  # прохождение неразделенных на сабкейсы записей.
        if points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):] == cur_mach:  # Если сабкейсы не изменился
            points.append(pd.DataFrame(points_temp[i][2:], columns=points_temp[i][1], dtype=float))
            cur_mach = points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):]
        else: # Если сабкейсы изменился, значит надо сохранить всё, что накопилось в прошлом сабкейсе
            dict_points[float(cur_mach[12:])] = points
            cur_mach = points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):]
            points = []
        if i == len(points_temp) - 1:  # Обработка самого последнего сабкейса. Т.к. для последнего нет изменения
            dict_points[float(points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER') + 12:])] = points

    # Убирание лишних колонок
    if clear_columns:
        for key in dict_points:
            for df in dict_points[key]:
                df.drop(['KFREQ', '1./KFREQ', 'COMPLEX', 'EIGENVALUE'], axis=1, inplace=True)

    return dict_points


dct = get_points('rv_30_surf_all_fl_m085_089.f06')

print(dct.keys())
points = dct[0.89]
print(points[0].columns)
print(points[0])


# for i in dct:  # Проход по всем Махам
# for j in dct[i]:  # Проход по всем тонам
# print(j)

fig = plt.figure()
for i in range(len(points)):
    plt.plot(points[i]['DAMPING'], points[i]['FREQUENCY'])
plt.grid()
plt.show()

fig = plt.figure()
for i in range(len(points)):
    plt.plot(points[i]['VELOCITY'], points[i]['DAMPING'])
plt.grid()
plt.show()



