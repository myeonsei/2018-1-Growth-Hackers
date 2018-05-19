import pandas as pd; import statsmodels.formula.api as smf
dirr = 'C:\\test\\reg_quest.csv'
data = pd.read_csv(dirr)

OLS = smf.ols('symtot ~ income + age + black + clinic', data = data).fit()
print(OLS.summary())
