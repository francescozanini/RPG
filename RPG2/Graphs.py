import pandas as pd
import matplotlib as plt

enemy_table_df = pd.read_csv('enemy_table.csv', index_col=0)

grouped_enemies = enemy_table_df.groupby(['HPs'])
print(grouped_enemies.groups)

grouped_enemies.plot()

fig, ax = plt.subplots()
for name,group in grouped_enemies:
    print group
    ax.bar(name, group['MPs'].expanding(min_periods = 3).mean().iloc[max(3, int(name/20))]), 350, alpha=0.4, yerr

ax.set_xlabel('HPs')
ax.set_ylabel('MPs')
ax.set_title('')

labels=[20, 416, 812, 1208, 1604, 2000]
sizes=grouped_enemies['APs'].agg(np.max).values
explode=tuple(i/10 for i in range(len(labels)))

fig1, ax1=plt.subplots()
ax1.pie(sizes, explode=explode, labels=lables, autopct='%1.1%%', shadow=Treu, startangle=90)