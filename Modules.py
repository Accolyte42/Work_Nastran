import pandas as pd
import matplotlib.pyplot as plt


def merge_two_dicts(lst):
    z = lst[0].copy()
    for i in range(1, len(lst)):
        z.update(lst[i])
    return z


def read_points_from_file(filename):
    # Функция чтения всех тонов для всех сабкейсов без разделения
    flut_flag = False  # Флаг, отвечающий за начало расчета на флаттер в f06 файле
    count_point = 3  # номер строки, с которой идет описание случая
    count_data = 5  # номер строки, с которой идут данные (с шапкой)
    counter_row = 0  # счетчик строк для определения информативных
    points_temp = []  # Расчетные точки. Каждая расчетная точка - двумерный массив

    # После чтения всего файла получаем points_temp - это все расчетные точки подряд для всех махов (subcase-ов)
    with open(filename) as file:
        for line in file:
            line = line.strip()  # убирание лишних пробелов с начала и конца

            if 'FLUTTER' and 'SUMMARY' in line:  # если встретили нужный блок с началом флаттера
                flut_flag = True  # Если начался флаттерная часть
                counter_row = 1  # теперь мы можем считать строки в информативном блоке
                pnt = []  # текущая точка

            # Пока мы в нужном блоке
            while flut_flag and (counter_row == count_point or counter_row > count_data):  # Пока мы в нужном блоке
                if 'NASTRAN' and 'AEROELASTIC' in line:  # Определение условия выхода из блока
                    flut_flag = False
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

    return points_temp


def get_points(filename, clear_columns=True):
    # Функция, принимающая (полное) имя файла, и выдающая словарь со всеми

    # После чтения всего файла получаем points_temp - это все расчетные точки подряд для всех махов (subcase-ов)
    points_temp = read_points_from_file(filename)

    # Далее надо разделить points_temp по сабкейсам (разным махам)
    points = []  # Это уже точки в каждом сабкейсе
    cur_mach = points_temp[0][0][0][points_temp[0][0][0].index('MACH_NUMBER'):]
    dict_points = {}

    # Далее неразделенные записи points_temp деляться на записи по сабкейсам в словарь
    for i in range(len(points_temp)):  # прохождение неразделенных на сабкейсы записей.
        if points_temp[i][0][0][
           points_temp[i][0][0].index('MACH_NUMBER'):] == cur_mach or flag_change:  # Если сабкейсы не изменился
            points.append(pd.DataFrame(points_temp[i][2:], columns=points_temp[i][1], dtype=float))
            cur_mach = points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):]
            flag_change = False
        else:  # Если сабкейсы изменился, значит надо сохранить всё, что накопилось в прошлом сабкейсе
            # points.append(pd.DataFrame(points_temp[i][2:], columns=points_temp[i][1], dtype=float))
            dict_points[float(cur_mach[12:])] = points
            cur_mach = points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER'):]
            points = []
            points.append(pd.DataFrame(points_temp[i][2:], columns=points_temp[i][1], dtype=float))
            flag_change = True
        if i == len(points_temp) - 1:  # Обработка самого последнего сабкейса. Т.к. для последнего нет изменения
            dict_points[float(points_temp[i][0][0][points_temp[i][0][0].index('MACH_NUMBER') + 12:])] = points

    # Убирание лишних колонок
    if clear_columns:
        for key in dict_points:
            for df in dict_points[key]:
                df.drop(['KFREQ', '1./KFREQ', 'COMPLEX', 'EIGENVALUE'], axis=1, inplace=True)

    return dict_points


def get_dct_tones(dct):
    flag_t = True
    dct_tones = {'test': pd.DataFrame({'test_mach': [.2, 1.1, 2.2]}, index=['e/2', 'e', 'f'])}
    for key in dct:
        counter = 0
        for pnts in dct[key]:
            if not flag_t:
                break
            dct_tones[counter] = pd.DataFrame({key: [.2, 1.1, 2.2]}, index=['e/2', 'e', 'f'])
            counter += 1
        counter = 0
        flag_t = False
    for key in dct:
        counter = 0
        for i in range(len(dct[key])):
            e = dct[key][i].iloc[len(dct[key][i]) // 2]['DAMPING']
            f = dct[key][i].iloc[len(dct[key][i]) // 2]['FREQUENCY']
            dct_tones[counter][key] = [e/2, e , f]
            counter += 1
        counter = 0
    dct_tones.pop('test')

    return dct_tones


def graphics_mach(dct, mach, tones='all'):
    # построение нужных графиков
    # Перенос индексов для красоты
    if tones != 'all':
        for i in range(len(tones)):
            tones[i] -= 1

    points = dct[mach]

    # plt.figure()
    plt.subplot(1, 2, 1)
    if tones == 'all':
        for i in range(len(points)):
            plt.plot(points[i]['DAMPING'], points[i]['FREQUENCY'], label=str(i+1) + 'тон')
    else:
        for i in tones:
            plt.plot(points[i]['DAMPING'], points[i]['FREQUENCY'], label=str(i+1) + 'тон')
    plt.title('DAMP-FREQ')
    plt.xlabel('DAMPING')
    plt.ylabel('FREQUENCY')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    if tones == 'all':
        for i in range(len(points)):
            plt.plot(points[i]['VELOCITY'], points[i]['DAMPING'], label=str(i+1) + 'тон')
    else:
        for i in tones:
            plt.plot(points[i]['VELOCITY'], points[i]['DAMPING'], label=str(i+1) + 'тон')
    plt.title('VEL-DAMP')
    plt.xlabel('VELOCITY')
    plt.ylabel('DAMPING')
    plt.legend()
    plt.grid(True)
    plt.show()


def graphics_dct(dcttt, ton_dct):

    plt.subplot(1, 2, 1)
    for mach in dcttt:
        counter = 0
        for n_tone in dcttt[mach]:
            plt.plot(n_tone['DAMPING'], n_tone['FREQUENCY'],
                     label=str(ton_dct[mach][counter]) + 'тон ' + str(mach) + 'МАХ')
            counter += 1
    plt.title('DAMP-FREQ')
    plt.xlabel('DAMPING')
    plt.ylabel('FREQUENCY')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    for mach in dcttt:
        counter = 0
        for n_tone in dcttt[mach]:
            plt.plot(n_tone['VELOCITY'], n_tone['DAMPING'],
                     label=str(ton_dct[mach][counter]) + 'тон ' + str(mach) + 'МАХ')
            counter += 1
    plt.title('VEL-DAMP')
    plt.xlabel('VELOCITY')
    plt.ylabel('DAMPING')
    plt.legend()
    plt.grid(True)
    plt.show()


def dct_from_files(filenames):
    dct = get_points(filenames[0])
    if len(filenames) > 1:
        for file in filenames:
            dct = merge_two_dicts([dct, get_points(file)])
    return dct


def cut_tones_by_upper_freq_dct(dct, freq=800):
    dctt = {}
    for mach in dct:
        flag = True
        dctt[mach] = []
        for n_tone in dct[mach]:
            if flag:
                for fr in n_tone['FREQUENCY']:
                    if fr > freq:
                        flag = False
                        break
                if flag:
                    dctt[mach].append(n_tone)
            else:
                break

    return dctt


def cut_tones_by_upper_freq_dct_tones(dct_tones, freq=800):
    dctt = {}
    flag = True
    for key in dct_tones:
        if flag:
            for i in dct_tones[key].columns:
                if dct_tones[key][i]['f'] > freq:
                    flag = False
                else:
                    dctt[key] = dct_tones[key]
        else:
            break

    return dctt


def cut_dangerous_tones_d(dct, dang_demp=-0.01):
    dctt = {}
    tones_dict = {}
    for mach in dct:
        tones = 0  # номер тона, нужен для того, чтобы при можно было понять, где какой тон
        tones_list = []
        dctt[mach] = []
        for n_tone in dct[mach]:
            # print(n_tone)
            tones += 1
            flag = True
            if flag:
                for dmp in n_tone['DAMPING']:
                    if dmp < dang_demp:
                        flag = False
                        break
                if flag:
                    dctt[mach].append(n_tone)
                    tones_list.append(tones)
            else:
                break
        tones_dict[mach] = tones_list

    return dctt, tones_dict


def print_e_f_table(dct_tones, filenames):
    # Красивый вывод  dct_tones. Это таблица с демпфированием и частотами для всех махов
    print()
    print('', end='')
    for files in filenames:
        print(files, end='')
    print()
    print()
    for key in dct_tones:
        print(str(key + 1) + 'Тон')
        print(dct_tones[key])
        print()