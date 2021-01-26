import pandas as pd
# import matplotlib.pyplot as plt
import random
import array



population=pd.read_csv('F:\Flask Server Python\westbengal2.csv',encoding='ISO-8859-1')
population.dropna(inplace=True)
# print(population.isnull().sum())
cities=list(population.City.unique())

peoples=[int(''.join(item)) for item in (num.split(',') for num in population['P-2011'].unique())]

data={'peoples':peoples,'cities':cities}

def color_code_generator(x):
    all_color_codes =[]
    for j in range(x):
        color_code=['#'+str(''.join(random.choice('0123456789ABCDEF') for i in range(6)))]
        all_color_codes.extend(color_code)
    return all_color_codes

if __name__ == '__main__':
    print(color_code_generator(5))

