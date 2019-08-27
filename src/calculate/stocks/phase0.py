import pandas as pd

df = pd.read_csv('data/phase0/IVE_tickbidask.txt')
df.columns = ['Date', 'Time', 'Open', 'Low', 'High', 'Volume']
for year in range(2015, 2020):
    yearStr = str(year)
    print('working on %s' % yearStr)
    curr_df = df[df['Date'].str.contains(yearStr)]
    curr_df.to_csv('data/phase1/IVE_tickbidask_' + yearStr + '.csv')
