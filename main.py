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
import Modules as m


def cut_tones_by_upper_freq_dct(dct, freq):
    dctt = {}
    for mach in dct:
        flag = True
        for n_tone in dct[mach]:
            if flag:
                for fr in n_tone['FREQUENCY']:
                    if fr > freq:
                        flag = False
                        break
                    else:
                        dctt[mach] = n_tone
            else:
                # print(n_tone)
                break

    return dctt


# def dangerous_tones()


# _________________________________________________________________________
# _________________________________________________________________________
# _______________________________Основная часть____________________________
# _________________________________________________________________________

# Ввод входных файлов
filenames = ['rv_30_surf_all_fl_m085_089.f06', 'rv_30_surf_all_fl_m09_new.f06']
dct = m.dct_from_files(filenames)

print(dct.keys())

dct = cut_tones_by_upper_freq_dct(dct, 600)
print(dct)

# dct_tones = m.get_dct_tones(dct)
# dct_tones = m.cut_tones_by_upper_freq_dct_tones(dct_tones, 600)

# Красивый вывод  dct_tones. Это таблица с демпфированием и частотами для всех махов
# m.print_e_f_table(dct_tones, filenames)

# m.graphics(dct, 0.89, [1,2,4])


