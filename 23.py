
# my_series2 = pd.Series([5, 6, 7, 8, 9, 10], index=['a', 'b', 'c', 'd', 'e', 'f'])
# print(my_series2)

dct_tones = {'test': pd.DataFrame({
    'test_mach': [1.1, 2.2]
    }, index=['e', 'f'])}
for key in dct:
    counter = 0
    for pnts in dct[key]:
        dct_tones[counter] = pd.DataFrame({key: [1.1, 2.2]}, index=['e', 'f'])
        counter += 1
