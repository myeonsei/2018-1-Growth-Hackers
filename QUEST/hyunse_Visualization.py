import pandas as pd; from matplotlib import pyplot as plt

df = pd.read_csv('C:\\Users\\myeon\\Desktop\\Data Science\\데이터시각화\\caschool.csv', engine='python')

plt.subplot(221)
plt.plot(df.math_scr, color='r', marker='x')
plt.legend(loc='best'); plt.title('Math Score'); plt.ylabel('score'); plt.grid(1)

plt.subplot(222)
plt.bar(df.obs, df.math_scr)
plt.bar(df.obs, df.read_scr, bottom=df.math_scr)
plt.title('Total Score'); plt.xlabel('county'); plt.ylabel('total'); plt.xticks(df.obs, df.county)

plt.subplot(223)
plt.hist(df.avginc, bins=30, color='orange', histtype='step')
plt.title('Average Income')

plt.subplot(224)
plt.style.use('ggplot')
plt.scatter(df.avginc, df.math_scr, s=1, c='k', alpha=.5)
plt.axvline(x=df.avginc.mean(), linestyle='dashed'); plt.axhline(y=df.math_scr.mean(), linestyle='dashed', color='b'); plt.title('Income & Math Score')

plt.show() 
