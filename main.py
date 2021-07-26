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
%matplotlib


def graph_flutt(dct_tones, lst_tones = 'all'):
    counter = 0
    if lst_tones == 'all':
        for tones in dct_tones:
            dct_tones[tones] = dct_tones[tones].T
            plt.plot(dct_tones[tones]['e'],dct_tones[tones]['f'], marker = 'o', label=str(tones+1))
    else:
        lst=[]
        for i in lst_tones:
            lst.append(i-1)
        for tones in lst:
            dct_tones[tones] = dct_tones[tones].T
            plt.plot(dct_tones[tones]['e'],dct_tones[tones]['f'], marker = 'o', label=str(tones+1))
    plt.legend()
    plt.title('DAMP-FREQ')
    plt.xlabel('DAMPING')
    plt.ylabel('FREQUENCY')
    plt.grid(True)
    plt.show()


def graph_flutt_test(dct_tones, lst_tones = 'all'):
    
    for tones in dct_tones:
        lst_mach = []
        for mach in dct_tones[tones]:
            lst_mach.append(mach)
        dct_tones[tones] = pd.concat([dct_tones[tones].T, pd.DataFrame({'Точки': lst_mach}, index = lst_mach)], axis=1)
    # print(dct_tones)
    
    if lst_tones == 'all':
        # print(dct_tones.keys())
        dct_tones_T = {}
        for tones in dct_tones:
            

            ax = plt.gca()
            # dct_tones_T[tones] = dct_tones[tones].T
            # print(dct_tones[tones].keys())
            # plt.annotate(dct_tones[tones]['Точки'], xy=(0,0), axis=1)
            dct_tones[tones].apply(lambda x: ax.annotate(x['Точки'], (x['e'] + 0.2, x['f'])), axis=1)
            plt.plot(dct_tones[tones]['e'],dct_tones[tones]['f'], marker = 'o', label=str(tones+1))
            print(dct_tones[tones])
    else:
        lst=[]
        for i in lst_tones:
            lst.append(i-1)
        for tones in lst:
            dct_tones[tones] = dct_tones[tones].T
            plt.plot(dct_tones[tones]['e'],dct_tones[tones]['f'], marker = 'o', label=str(tones+1))
    # print(dct_tones)
    
    plt.title('DAMP-FREQ')
    plt.xlabel('DAMPING')
    plt.ylabel('FREQUENCY')
    plt.grid(True)
    plt.show()
    
    

# _________________________________________________________________________
# _________________________________________________________________________
# _______________________________Основная часть____________________________
# _________________________________________________________________________

# Ввод входных файлов
filenames = ['rv_30_surf_all_fl_m085_089.f06']
dct = m.dct_from_files(filenames)

# print(dct.keys())

dct_cut_freq = m.cut_tones_by_upper_freq_dct(dct, 800)
dct_cut_freq_demp, tones_dict = m.cut_dangerous_tones_d(dct_cut_freq, -0.02)

dct_tones = m.get_dct_tones(dct)
dct_tones_cut = m.cut_tones_by_upper_freq_dct_tones(dct_tones, 800)

# Красивый вывод  dct_tones. Это таблица с демпфированием и частотами для всех махов
# m.print_e_f_table(dct_tones_cut, filenames)

# print(dct_tones_cut[0])

graph_flutt_test(dct_tones_cut)

# print(dct[0.9])

# m.graphics_dct(dct_cut_freq_demp, tones_dict)
# m.graphics_mach(dct, 0.85)


