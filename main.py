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



def get_points(filename, pnt_lst='all'):
    Flut_flag = False
    count_point = 3  # номер строки, с которой идет описание случая
    count_data = 5  # номер строки, с которой идут данные (с шапкой)
    counter_row = 0  # счетчик строк для определения информативных
    counter_points = 1  # счетчик расчетных точек
    points_temp = []  # Расчетные точки. Каждая расчетная точка - двумерный массив
    points_name_subcase = []

    with open(filename) as file:
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

                for i in range(20):  # Удаление лишних пробелов. Теперь отделение по одному пробелу
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

                pnt.append(
                    lst_str)  # прочитали всю строку, значит теперь можно список lst_str записать в текущую точку pnt

                break
            counter_row += 1

    points = []
    cur_Mach = points_temp[0][0][0][points_temp[0][0][0].index('MACH_NUMBER'):]
    dict_points = {}
    # print(cur_Mach)

    if pnt_lst == 'all':  # Если вывод всех тонов
        for i in range(len(points_temp)):
            # print(i)
            if points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):] == cur_Mach:
                points.append(pd.DataFrame(points_temp[i][2:], columns=points_temp[i][1], dtype=float))
                points_name_subcase.append(points_temp[i][0])
                cur_Mach = points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):]
            else:
                dict_points[float(cur_Mach[12:])] = points
                # print(cur_Mach)
                cur_Mach = points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):]
                points = []
                points_name_subcase = []
            if i == len(points_temp) - 1:
                dict_points[float(points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER') + 12:])] = points
                # print(cur_Mach)

    else:  # Если ввод определенных тонов
        for i in pnt_lst:
            points.append(pd.DataFrame(points_temp[i][2:], columns=points_temp[i][1], dtype=float))
            points_name_subcase.append(points_temp[i][0])

    return dict_points


dct = get_points('rv_30_surf_all_fl_m085_089.f06')

print(dct.keys())
points = dct[0.85]
print(points[0].columns)
# del points[0]['KFREQ'], points[0]['1./KFREQ'], points[0]['COMPLEX'], points[0]['EIGENVALUE']
print(points[0])
# print(len(dct))
# print(len(points))
# print(len(points[0]) // 2)


# for i in dct:  # Проход по всем Махам
# for j in dct[i]:  # Проход по всем тонам
# print(j)
# Comment

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

# Надо добавить оформление получше, выбор файла и выбор точек. Всё остальное запрятать