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

