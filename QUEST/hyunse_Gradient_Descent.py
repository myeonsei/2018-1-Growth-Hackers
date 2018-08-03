# ML Session 1 Quest

import numpy as np; import pandas as pd; from scipy import optimize as op; from matplotlib import pyplot as plt

df = pd.read_csv('C:\\Users\\myeon\\Desktop\\Data Science\\quest_tipping.csv')
df['d_SEX'] = (df['SEX'] == 'Female').apply(int)
n = len(df)

def cost_func(beta):
   j = 0
   for i in range(n):
       j += (df.loc[i, 'TIPRATE'] - beta[0] - beta[1] * df.loc[i, 'd_SEX'] - beta[2] * df.loc[i, 'TOTBILL']) ** 2
       
   return j

def y_hat(x, beta):
   return beta[0] + x[0] * beta[1] + x[1] * beta[2]

beta = op.minimize(cost_func, (1, 0, 0))['x']
print(beta)

xx = np.linspace(15, 20, 6)
male = y_hat((0, xx), beta); female = y_hat((1, xx), beta)
plt.plot(xx, male, 'k', color='orange')
plt.plot(xx, female, 'k', color='red')
